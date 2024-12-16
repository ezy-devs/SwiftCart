from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from Store.models import Category, Product
from .models import Cart, CartItem



def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)


        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

            cart_count = CartItem.objects.filter(cart=cart).count()
            response = JsonResponse({'message': 'Item added to cart', 'cart_count':cart_count})
            messages.success(request, response)
            return response
    
    return JsonResponse({'error': 'Invalid request'}, status=400)




def cart_summary(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
    cart_items = cart.items.all()
    context = {
            'categories':categories,
            'cart':cart,
            'cart_items':cart_items,
        }
        
    return render(request, 'cart/cart_summary.html', context)

def fetch_cart(request):
    if request.method == 'GET':

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()

            cart = Cart.objects.filter(session_key=request.session.session_key).first()
        cart_items = []
        if cart:
            # if item.product.is_sale: 
            #     final_price = item.product.sale_price 
            # else:
            #     final_price = item.product.price
            cart_item_list = cart.items.all()

            cart_items = [
                
                {
                'product_id': item.product.id,
                'product_image': item.product.image.url,
                'product_name': item.product.name,
                'description': item.product.description,
                'quantity': item.quantity,
                'total_price': item.quantity * item.product.price,
            }

            
            for item in cart_item_list
            ]
        return JsonResponse({'cart_items': cart_items})


def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                session_key = request.session.create()
                cart = Cart.objects.filter(session_key=request.session.session_key)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
       
        return JsonResponse({'response': 'Item updated!'})


class MergeCartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key
            if session_key:
                guest_cart = Cart.objects.get_or_create(session_key=session_key).first()
                if guest_cart:
                    user_cart, created = Cart.objects.get_or_create(user=request.user)
                    for item in guest_cart.items.all():
                        user_item = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
                        if not created:
                            user_item.quantity += item.quantity
                            user_item.save()
                    guest_cart.delete()


def remove_item(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            item = CartItem.objects.get(cart=cart, product=product)

        else:
            session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key)
            item = CartItem.objects.get(cart=cart, product=product)

        item.delete()

        response = JsonResponse({'message': 'Item removed'})
        
        messages.success(request, 'Item removed')
        return response
    response = JsonResponse({'message': 'Unable to process request'})
    messages.success(request, response)
    return response