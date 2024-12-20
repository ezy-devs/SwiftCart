from django.shortcuts import render, redirect
from django.contrib import messages

from Store.models import Category
from Cart.models import Cart, CartItem
from .forms import ShippingForm, PaymentForm
from .models import ShippingInfo, Order, OrderItem


def update_shipping_info(request):
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
            
            messages.success(request, 'Shipping info updated successfully!')
            # return redirect('profile', request.user.username if request.user.is_authenticated else 'guest')
            return redirect(update_shipping_info)
        else:
            messages.error(request, 'could not process request, try again!')
            return redirect(update_shipping_info)
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
    total_price = 0.0
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

    context = {
            'categories':categories,
            'cart':cart,
            'cart_items':cart_items,
            'total_price':total_price,
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

# def process_order(request):
#     if request.POST:
#         categories = Category.objects.all()
        
#         my_shipping = request.session.get('my_shipping')

#         shipping_address = f"{my_shipping['shipping_full_name']}\n{my_shipping['shipping_email']}\n{my_shipping['shipping_phone_number']}\n{my_shipping['shipping_address_1']}\n{my_shipping['shipping_address_2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_postal_code']}\n{my_shipping['shipping_country']}"

#         full_name = my_shipping['shipping_full_name']
#         email = my_shipping['shipping_email']
#         shipping_address = f"{my_shipping['shipping_address_1']} - {my_shipping['shipping_address_2']}"
        
#         total_price = 0.0
#         if request.user.is_authenticated:
#             user = request.user
#             cart = Cart.objects.filter(user=user).first()
            
#             if cart:
            
#                 cart_item_list = cart.items.all()
#                 for item in cart_item_list:
                    
#                     if item.product.is_sale:
#                         price = item.product.sale_price
#                     else:
#                         price = item.product.price
#                     item_total =  item.quantity * price
                    
#                     total_price += float(item_total)

#             create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address)
#             order = create_order.save(commit=False)
#             order.amount_paid = total_price
#             order.save()
#             messages.error(request, 'Order placed')
#             return redirect('home')
            
#         else:
#             session_key = request.session.session_key
#             cart = Cart.objects.filter(session_key=session_key).first()

        
#             if cart:
                
#                 cart_item_list = cart.items.all()
#                 for item in cart_item_list:
                    
#                     if item.product.is_sale:
#                         price = item.product.sale_price
#                     else:
#                         price = item.product.price
#                     item_total =  item.quantity * price
                    
#                     total_price += float(item_total)

            
#             create_order = Order.objects.create(session_key=session_key, full_name=full_name, email=email, shipping_address=shipping_address)
#             order = create_order.save(commit=False)
#             order.amount_paid = total_price
#             order.save()
        
#             messages.error(request, 'Order placed')
#             return redirect('home')

#         print(create_order)
        


        
    
#     else:
#         messages.error(request, 'Access denied!')
#         return redirect('home')


    

def payment_success(request):
    pass

def process_order(request):
    if request.method == "POST":
        categories = Category.objects.all()
        my_shipping = request.session.get('my_shipping')

        if not my_shipping:
            messages.error(request, 'Shipping details not found.')
            return redirect('home')

        # Construct shipping address
        shipping_address = (
            f"{my_shipping.get('shipping_address_1')} - {my_shipping.get('shipping_address_2')}, "
            f"{my_shipping.get('shipping_city')}, {my_shipping.get('shipping_state')}, "
            f"{my_shipping.get('shipping_country')} - {my_shipping.get('shipping_postal_code')}"
        )
        full_name = my_shipping.get('shipping_full_name')
        email = my_shipping.get('shipping_email')

        total_price = calculate_cart_total(request)

        if total_price is None:
            messages.error(request, "Cart is empty. Cannot place an order.")
            return redirect('home')

        # Create order
        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_price,
            )
        else:
            session_key = request.session.session_key
            if not session_key:
                messages.error(request, "Session expired. Please try again.")
                return redirect('home')

            order = Order.objects.create(
                session_key=session_key,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_price,
            )

        messages.success(request, 'Order placed successfully!')
        return redirect('home')
    else:
        messages.error(request, 'Access denied!')
        return redirect('home')


def calculate_cart_total(request):
    """
    Calculates the total price of items in the cart for the current user or session.
    """
    total_price = 0.0
    cart = None

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()

    if not cart or not cart.items.exists():
        return None

    for item in cart.items.all():
        price = item.product.sale_price if item.product.is_sale else item.product.price
        total_price += item.quantity * float(price)

    return total_price
