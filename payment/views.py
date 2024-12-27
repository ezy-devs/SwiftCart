from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.urls import reverse
import json
import requests
from Store.models import Category, Product
from Cart.models import Cart, CartItem
from .forms import ShippingForm, PaymentForm
from .models import ShippingInfo, Order, OrderItem
from .utills import calculate_cart_total

from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
import uuid

paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)



def initiate_payment(request):
    my_shipping = request.session.get('my_shipping')
    if not my_shipping:
        messages.error(request, 'Shipping info not found')
        return redirect('cart')
    
    # Construct shipping info
    shipping_address = (
        f"{my_shipping.get('shipping_address_1')} - {my_shipping.get('shipping_address_2')}, "
        f"{my_shipping.get('shipping_city')}, "
        f"{my_shipping.get('shipping_state')}, "
        f"{my_shipping.get('shipping_country')}"
    )
    full_name = my_shipping.get('shipping_full_name')
    email = my_shipping.get('shipping_email')

    total_amount = calculate_cart_total(request)
    if total_amount is None:
        messages.error(request, 'Cart is empty, cannot place an order')
        return redirect('cart')
    
    if request.method == 'POST':
        # Get the amount and user info
        if request.user.is_authenticated:
            user = request.user

            try:
                total_amount = int(float(total_amount) * 100)
            except ValueError:
                messages.error(request, 'Invalid amount')
                return redirect('cart')

            reference = str(uuid.uuid4())

            order = Order.objects.create(
                user=user,
                amount_paid=total_amount / 100,  # Save the amount in naira
                reference=reference,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
            )
            
            
            
        # Initiate Paystack payment
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',  
        }
        data = {
            'full_name':full_name,
            'email': email,
            'amount': total_amount,  # Send amount in kobo
            'reference': reference,
            'callback_url': request.build_absolute_uri(reverse('verify-payment')),
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json().get('data', {})
            authorization_url = response_data.get('authorization_url', '')
            trxref = response_data.get('reference', '')
            
            
            if authorization_url and trxref:
                return redirect(f"{authorization_url}?trxref={trxref}&reference={trxref}")
            
            else:
                messages.error(request, 'Unable to retrieve payment URL')
                return redirect('cart')
        else:
            error_message = response.json().get('message', 'Payment initialization failed')
            messages.error(request, error_message)
            return redirect('cart')
    
    return render(request, 'payment/initiate_payment.html', {
        'shipping_info': my_shipping,
        'total_amount': total_amount,
    })


def verify_payment(request):
    trxref = request.GET.get('trxref')
    reference = request.GET.get('reference')

    if not trxref or not reference:
        messages.error(request, 'Transaction reference or reference missing.')
        return redirect('cart')

    url = f"https://api.paystack.co/transaction/verify/{trxref}"
    headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get('data', {})
        status = data.get('status')
        order = get_order(request, reference)

        if not order:
            return redirect('cart')

        if status == 'success':
            cart = get_cart(request)
            if cart:
                handle_cart_items(cart, order)
            messages.success(request, 'Payment successful!')
            
            return redirect(f"{reverse('payment_success')}?reference={reference}")
        else:
            messages.error(request, 'Payment verification failed.')
    else:
        messages.error(request, 'Error verifying payment with Paystack.')

    return redirect('cart')

def handle_cart_items(cart, order):
    items = cart.items.all()
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.product.price,
            quantity=item.quantity,
        )
    items.delete()


def get_order(request, reference):
    if request.user.is_authenticated:
        user = request.user
        order = get_object_or_404(Order, user=user, reference=reference)
    else:
        session_key = request.session.session_key
        if not session_key:
            messages.success(request, 'Session expired, please try again')
            return None
        order = get_object_or_404(Order, session_key=session_key, reference=reference)
    return order

def get_cart(request):
    cart = Cart.objects.filter(user=request.user).first() if request.user.is_authenticated else Cart.objects.filter(session_key=request.session.session_key).first()
    return cart

@csrf_exempt
def paystack_webhook(request):
    if request.method == 'POST':
        event = json.loads(request.body)
        if event['event'] == 'charge.success':
            reference = event['data']['reference']
            # Update payment status in your database
            # ...
        return HttpResponse(status=200)
    return HttpResponse(status=400)


def shipping_info(request):
    if request.user.is_authenticated:
        shipping_info = ShippingInfo.objects.filter(user=request.user).first()

    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        shipping_info = ShippingInfo.objects.filter(session_key=session_key).first()

    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping_info)
        if form.is_valid():
            shipping_instance = form.save(commit=False)
            if request.user.is_authenticated:
                shipping_instance.user = request.user
            else:
                shipping_instance.session_key = request.session.session_key
            shipping_instance.save()

            my_shipping = request.POST
            request.session['my_shipping'] = my_shipping
            
            print(my_shipping)
            messages.success(request, 'Shipping info updated successfully!')
            cart_total = float(request.session['cart_total'])
            return redirect(f"{reverse('initiate_payment')}?amount={cart_total}")
        else:
            messages.error(request, 'could not process request, try again!')
            return redirect('shipping_info')
    else:
        form = ShippingForm(instance=shipping_info)

    return render(request, 'payment/shipping_form.html', {'form': form})


def checkout(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        shipping_info = ShippingInfo.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()
        shipping_info = ShippingInfo.objects.filter(session_key=session_key).first()
    cart_items = []
    total_amount = 0.0
    if cart:
        
        cart_item_list = cart.items.all()
        for item in cart_item_list:
            
            if item.product.is_sale:
                price = item.product.sale_price
            else:
                price = item.product.price
            item_total =  item.quantity * price
            
            total_amount += float(item_total)
            request.session['cart_total'] = total_amount
           
            print('Total price: ' + str(total_amount))

            cart_items.append({
                    'product_id': item.product.id,
                    'product_image': item.product.image.url,
                    'product_name': item.product.name,
                    'description': item.product.description,
                    'quantity': item.quantity,
                    'item_price': item_total,
                    
                })
            # request.session.create('cart_items') = cart_items
            
        
    cart_items.reverse()
    shipping_form = ShippingForm(instance=shipping_info)

    context = {
            'categories':categories,
            'cart':cart,
            'cart_items':cart_items,
            'cart_total':total_amount,
            'shipping_form':shipping_form,
        }
    return render(request, 'payment/checkout.html', context)


def billing_info(request):
    if request.POST:
        categories = Category.objects.all()
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            shipping_info = ShippingInfo.objects.filter(user=request.user).first()
            billing_form = PaymentForm()
            
        else:
            session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first()
            shipping_info = ShippingInfo.objects.filter(session_key=session_key).first()
            billing_form = PaymentForm()
        cart_items = []
        total_price = 0.0
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        if cart:
            
            cart_item_list = cart.items.all()
            for item in cart_item_list:
                
                if item.product.is_sale:
                    price = item.product.sale_price
                else:
                    price = item.product.price
                item_total =  item.quantity * price
                
                total_price += float(item_total)
                
                cart_items.append({
                        'product_id': item.product.id,
                        'product_image': item.product.image.url,
                        'product_name': item.product.name,
                        'description': item.product.description,
                        'quantity': item.quantity,
                        'total_price': item_total,
                        
                    })
                print(cart_items)
            
        cart_items.reverse()
        shipping_form = ShippingForm(instance=shipping_info)

        return render(request, 'payment/billing_info.html', {'categories':categories, 'cart':cart, 'cart_items':cart_items, 'shipping_info':shipping_info, 'billing_form':billing_form, 'total_price':total_price,})
    else:
        messages.error(request, 'Access denied!')
        return redirect('home')
    

def payment_success(request):
    reference = request.GET.get('reference')
    cart = get_cart(request)
    order = get_order(request, reference)
    order_item = handle_cart_items(cart, order)

    return render(request, 'payment/payment_success.html', {
        'reference': reference,
        'order':order,
        'order_item':order_item,
    })

def process_order(request):
    if request.method == 'POST':
        my_shipping = request.session.get('my_shipping')
        if not my_shipping:
            messages.error(request, 'Shipping info not found')
            return redirect('home')
        
        # construct shipping info
        shipping_address = (
            f"{my_shipping.get('shipping_address_1')} - {my_shipping.get('shipping_address_1')}",
            f"{my_shipping.get('shipping_city')}",
            f"{my_shipping.get('shipping_state')}",
            f"{my_shipping.get('shipping_country')}"
        )
        full_name = my_shipping.get('shipping_full_name')
        email = my_shipping.get('shipping_email')

        total_price = calculate_cart_total(request)
        if total_price is None:
            messages.error(request, 'Cart is empty, cannot place an order')
            return redirect('cart')
        
        # create order
        if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.filter(user=user).first()
            if cart:
                # create order
                order = Order.objects.create(user=user, full_name=full_name, email=email, shipping_address=shipping_address)            
                order.amount_paid = total_price
                order.save()
                # create order item
                items = cart.items.all()
                for item in items:
                    order_item = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                    order_item.save()
                items.delete()

        else:
            session_key = request.session.session_key
            if not session_key:

                messages.success(request, 'Session expired, please try again')
                return redirect('home')
            cart = Cart.objects.filter(session_key=session_key).first()
            if cart:
                # Create order
                order = Order.objects.create(session_key=session_key, full_name=full_name, email=email, shipping_address=shipping_address)
                order.amount_paid = total_price
                order.save()

                # create order item
                items = cart.items.all()
                for item in items:
                    order_item = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                    order_item.save()
            items.delete()
            
        messages.success(request, 'Order placed successfully!')
        return redirect('cart')

    else:
        messages.error(request, 'Access denied!')
        return redirect('home')

# def get_order(request, reference):
#     if request.user.is_authenticated:
#         user = request.user
#         order = get_object_or_404(Order, user=user, reference=reference)
#     else:
#         session_key = request.session.session_key
#         if not session_key:
#             messages.success(request, 'Session expired, please try again')
#             return redirect('home')
#         order = get_object_or_404(Order, session_key=session_key, reference=reference)
    
#     return order

