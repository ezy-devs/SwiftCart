from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.deprecation import MiddlewareMixin
from Store.models import Category, Product
from .models import Cart, CartItem



def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get('quantity', 1)

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

    return JsonResponse({'message': 'Item added to cart!'})

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