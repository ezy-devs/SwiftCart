from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from Store.models import Category, Product
from .models import Cart, CartItem
# from .forms import ShippingForm



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
                session_key = request.session.create()
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

            cart_count = CartItem.objects.filter(cart=cart).count()
           
            return JsonResponse({'message': 'Item added to cart', 'cart_count':cart_count})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)




def cart_summary(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        
        cart = Cart.objects.filter(session_key=session_key).first()

    if cart:
        cart_items = cart.items.all()
    else:
        cart_items = []
    context = {
            'categories':categories,
            'cart':cart,
            'cart_items':cart_items,
            # 'total_price':total_price,
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
            
        cart_items.reverse()
        return JsonResponse({'cart_items': cart_items, 'total_price': total_price})


def update_cart(request):
    if request.method == 'POST':
        
        try:
            product_id = request.POST.get('product_id')
            print('product id', product_id)
            new_quantity = int(request.POST.get('quantity', 1))
            print('q', new_quantity)
            
            if new_quantity <=0:
                return JsonResponse({'error': 'quantity must be aleast one'})
            
            product = get_object_or_404(Product, id=product_id)
            print('product fetched', product.name)
            if request.user.is_authenticated:
                print('user', request.user)
                cart, _ = Cart.objects.get_or_create(user=request.user)

            else:
                session_key = request.session.session_key
                print('key', session_key)
                if not session_key:
                    request.session.create()
                cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
            
            cart_item, created= CartItem.objects.get_or_create(cart=cart, product=product)
            print('cart item', cart_item, 'created', created)

            if not created:
                cart_item.quantity += new_quantity
                cart_item.save()
            else:
                cart_item.quantity += new_quantity
                cart_item.save()
                # cart_item = CartItem.objects.create(cart=cart, product=product, quantity=new_quantity)
            return JsonResponse({
                'message': 'Item updated!',
                'new_total_price':cart_item.quantity * cart_item.product.price
            })
           
        except ValueError as e:
           
            return JsonResponse({'error': f'Invalid input {str(e)}'}, status=400)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)


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
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first()
        
        if cart:
            item = CartItem.objects.filter(cart=cart, product=product).first()
            if item:
                item.delete()
                # messages.success(request, 'Item removed')
                return JsonResponse({'message': 'Item removed'})
            else:
                # messages.error(request, 'Item not found in cart')
                return JsonResponse({'message': 'Item not found in cart'}, status=404)
        else:
            # messages.error(request, 'Cart not found')
            return JsonResponse({'message': 'Cart not found'}, status=404)
    
    # messages.error(request, 'Invalid request method')
    return JsonResponse({'message': 'Invalid request method'}, status=400)

# def remove_item(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         product = get_object_or_404(Product, id=product_id)
#         if request.user.is_authenticated:
#             cart = Cart.objects.filter(user=request.user).first()
#             # item = CartItem.objects.get(cart=cart, product=product)

#         else:
#             session_key = request.session.session_key
#             if not session_key:
#                 session_key = request.session.create()

#             cart = Cart.objects.filter(session_key=session_key)
#         if cart:

#             item = CartItem.objects.get(cart=cart, product=product).first()
#             if item:
#                 item.delete()
#                 return JsonResponse({'message': 'Item removed'})
#             else:
#                 return JsonResponse({'error': 'Item not found'}, status=404)
            
#         else:
#             return JsonResponse({'error': 'Cart not found'}, status=404)
        
#     return JsonResponse({'error': 'Invalid request'}, status=405)






# @login_required
# def order_success(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     return render(request, 'order_success.html', {'order': order})
