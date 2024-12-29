from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateProductForm,EditProductForm
from Store.models import Product
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from payment.models import Order, OrderItem
from .forms import EditOrderForm,EditOrderItemForm
from django.contrib.auth.decorators import user_passes_test



def admin_check(user):
    return user.is_superuser

@user_passes_test(admin_check, login_url='home')
def dashboard(request):

    users = User.objects.all()
    recent_orders = Order.objects.order_by('-date_ordered')[:6]
    orders = Order.objects.all()
    context = {
        'users':users,
        'recent_orders':recent_orders,
        'orders':orders,
    }
    return render(request, 'dashboard/index.html', context)

@user_passes_test(admin_check, login_url='home')
def users(request):
    users = User.objects.all()
    return render(request, 'dashboard/users.html', {'users':users})


@user_passes_test(admin_check, login_url='home')
def delete_user(request, user_id):
    user = User.objects.filter(id=user_id)
    user.delete()
    return redirect('users')


@user_passes_test(admin_check, login_url='home')
def de_activate_user(request, user_id):
    user = User.objects.filter(id=user_id)
    user.is_active = False
    
    return redirect('users')


@user_passes_test(admin_check, login_url='home')
def products(request):
    products = Product.objects.all()
    # print(products)
    return render(request, 'dashboard/products.html', {'products':products})


@user_passes_test(admin_check, login_url='home')
def create_product(request):
    if request.method == 'POST':

        form = CreateProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            
            messages.success(request, "Product added successfully!")  
            return redirect('creare_product')  
        
        else:
            messages.error(request, "There was an error with the form. Please check the details and try again.")
 
    else:
        form = CreateProductForm()
    
    return render(request, 'dashboard/create_product.html', {'form': form})


@user_passes_test(admin_check, login_url='home')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        edit_form = EditProductForm(request.POST, request.FILES, instance=product)
        if edit_form.is_valid():
            edit_form.save()
            
            messages.success(request, "Product Updated successfully!")  
            
            return redirect('dashboard')  
        else:
            messages.error(request, "There was an error with the form. Please check the details and try again.")
    
    else:
        edit_form = EditProductForm(instance=product)
    
    
    return render(request, 'dashboard/edit_product.html', {'edit_form': edit_form, 'product':product})


@user_passes_test(admin_check, login_url='home')
def delete_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        product = get_object_or_404(Product, id=product_id)
        if product:
            product.delete()
            return JsonResponse({'message': 'Product deleted!'})
        else:
            return JsonResponse({'message': 'error occured, try again'})
    else:
        return JsonResponse({'message': 'Invalid request method'})
    

@user_passes_test(admin_check, login_url='home')
def orders(request):
    orders = Order.objects.all()
    
    for order in orders:

        order_item = OrderItem.objects.filter(order=order)

    return render(request, 'dashboard/orders.html', {'orders':orders})


@user_passes_test(admin_check, login_url='home')
def order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    order_items = OrderItem.objects.filter(order=order)
    order_form = EditOrderForm(instance=order)
   
    for item in order_items:
        item_form = EditOrderItemForm(instance=item)

    
    return render(request, 'dashboard/order.html', 
                  {'order':order, 'order_items':order_items,
                   })


@user_passes_test(admin_check, login_url='home')
def update_order(request):
    order_id = request.POST.get('order_id')
    order_status = request.POST.get('order_status')
    try:
        order = Order.objects.filter(id=order_id).first()
        if order:

            order.status = order_status
            order.save()
            return JsonResponse({'message': 'Order status updated!'})
        else:
            return JsonResponse({'message': 'Order not found!'})
    except Exception as e:
        return JsonResponse({'message': str(e)})

@user_passes_test(admin_check, login_url='home')
def get_recent_orders(request):
   
    recent_orders = Order.objects.all().order_by('-date_ordered')[:10]  # Adjust the query as needed
    orders_data = [
        {
            'id': order.id,
            'user': order.user.username if order.user else 'Guest',
            'amount_paid': order.amount_paid,
            'status': order.get_status_display(),
            'date_ordered': order.date_ordered.strftime('%Y-%m-%d %H:%M:%S'),
            'status_choices': order.STATUS_CHOICES
        }
        for order in recent_orders
    ]
    all_orders = Order.objects.all()
    all_orders_data = [
        {
            'id': order.id,
            'user': order.user.username if order.user else 'Guest',
            'amount_paid': order.amount_paid,
            'status': order.get_status_display(),
            'date_ordered': order.date_ordered.strftime('%Y-%m-%d %H:%M:%S'),
            'status_choices': order.STATUS_CHOICES
        }
        for order in all_orders
    ]

    return JsonResponse({'orders': orders_data, 'all_orders':all_orders_data})


@user_passes_test(admin_check, login_url='home')
def reports(request):
    return render(request, 'dashboard/reports.html', {})


@user_passes_test(admin_check, login_url='home')
def delete(request, pk, Model):
    result = get_object_or_404(Model, id=pk)
    result.delete()
    return result


@user_passes_test(admin_check, login_url='home')
def settings(request):

     return render(request, 'dashboard/settings.html', {})

