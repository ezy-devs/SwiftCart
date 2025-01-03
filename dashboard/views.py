from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateProductForm,EditProductForm
from Store.models import Product
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse
import requests
import openpyxl
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from payment.models import Order, OrderItem
from Store.models import Category
from .forms import EditOrderForm,EditOrderItemForm, NewCategoryForm, EditCategoryForm, EditProductForm, CreateProductForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import make_naive
from django.db.models import Q
from django.views import View
from django.db.models import Count
from Auth.forms import UpdateProfileForm
from payment.models import ShippingInfo
from payment.forms import ShippingForm

from django.db.models.functions import ExtractMonth



class UserDataView(View):
    def get(self, request):
        try:
            user_data = User.objects.annotate(month=ExtractMonth('date_joined')).values('month').annotate(count=Count('id')).order_by('month')

            print("User data:", user_data)

            labels_first_half = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
            labels_second_half = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            user_counts_first_half = [0] * 6
            user_counts_second_half = [0] * 6

            for entry in user_data:
                month = int(entry['month']) - 1  # Convert month to zero-based index
                if 0 <= month < 6:
                    user_counts_first_half[month] = entry['count']
                elif 6 <= month < 12:
                    user_counts_second_half[month - 6] = entry['count']

            data = {
                "labels_first_half": labels_first_half,
                "userData_first_half": user_counts_first_half,
                "labels_second_half": labels_second_half,
                "userData_second_half": user_counts_second_half
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def admin_check(user):
    return user.is_superuser

def view_profile(request, username):
    try:
        user = get_object_or_404(User, username=username)

        
    except User.objects.get(username=username).DoesNotExist:
        messages.error(request, 'User not found, please Login')
        return redirect('login')
    
    form = UpdateProfileForm(instance=user.profile)
    try:

        user_shipping_info = ShippingInfo.objects.filter(user=user).first()
        shipping_Form = ShippingForm(instance=user_shipping_info)

    except ShippingInfo.objects.filter(user=request.user).DoesNotExist:
        shipping_Form = ShippingForm()
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('view_profile', user)
        else:
            messages.success(request, 'Request could not be completed, try again!')
            return redirect('view_profile', user)

    return render(request, 'dashboard/view_profile.html', {'user': user, 'form':form, 'shipping_Form':shipping_Form})


def search(request):
    if request.method == 'GET':

        query = request.GET.get('q', '')
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        orders = Order.objects.filter(
            Q(email__icontains=query) |
            Q(reference__icontains=query) |
            Q(date_ordered__icontains=query)
        )

        categories = Category.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
            )
        results = chain(products, orders, categories, users)

        context = {
            'query':query,
            'results':results,
        }
        
        return render(request, 'dashboard/all_search.html', context)
    else:
        messages.error(request, 'Please enter a query.')
        return redirect('dashboard')

@user_passes_test(admin_check, login_url='home')
def dashboard(request):

    users = User.objects.all()
    recent_orders = Order.objects.order_by('-date_ordered')[:6]
    orders = Order.objects.all()
    pending_orders = orders.filter(status__iexact='pending')
    processing_orders = Order.objects.filter(status__iexact='processing')
    shipped_orders = Order.objects.filter(status__iexact='shipped')
    delivered_orders = Order.objects.filter(status__iexact='delivered')
    cancelled_orders = Order.objects.filter(status__iexact='cancelled')
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'users':users,
        'recent_orders':recent_orders,
        'orders':orders,
        'pending_orders':pending_orders,
        'processing_orders':processing_orders,
        'shipped_orders':shipped_orders,
        'delivered_orders':delivered_orders,
        'cancelled_orders':cancelled_orders,
        'categories':categories,
        'products':products,
    }
    return render(request, 'dashboard/index.html', context)

@user_passes_test(admin_check, login_url='home')
def users(request):
    users = User.objects.all()
    return render(request, 'dashboard/users.html', {'users':users})


@user_passes_test(admin_check, login_url='home')
def download_users_excel(request):

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'User list'

    
    sheet.append(['Username', 'Email', 'First Name', 'Last Name', 'Admin Status', 'Date Joined'])

    users = User.objects.all()

    for user in users:
        naive_date_joined = make_naive(user.date_joined)
        sheet.append([user.username, user.email, user.first_name, user.last_name, user.is_superuser, naive_date_joined])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename"user_list.xlsx"'
    workbook.save(response)
    return response


@user_passes_test(admin_check, login_url='home')
def new_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        is_admin = request.POST.get('is_admin', False)
        
        if password:

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already used')
                return redirect('new_user')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'username already used')
                return redirect('new_user')
            elif is_admin:
                user = User.objects.create_superuser(username=username, email=email, password=password)
            else:
                user = User.objects.create_user(username=username, email=email, password=password)

            user.save()
            messages.success(request, 'User created successfully!')
            return redirect('new_user')
        
        else:
            messages.error(request, 'Password field can not be empty')
            return redirect('new_user')

    else:
        return render(request, 'dashboard/new_user.html')

@user_passes_test(admin_check, login_url='home')
def delete_user(request, user_id):
    user = User.objects.filter(id=user_id)
    user.delete()
    return redirect('users')


@user_passes_test(admin_check, login_url='home')
def deactivate_user(request, user_id):
    if request.method == 'POST':

        try:
            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()
            messages.success(request, f"User {user.username} has been deactivated.")
            return redirect('users')
        except User.DoesNotExist:
            messages.success(request, f"User {user.username} does not exist.")
            return redirect('users')
    else:
        messages.success(request, 'Invalid request method.')
        return redirect('users')

def activate_user(request, user_id):
    if request.method == 'POST':

        try:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            messages.success(request, f"User {user.username} has been activated.")
            return redirect('users')
        except User.DoesNotExist:
            messages.success(request, f"User {user.username} does not exist.")
            return redirect('users')
    else:
        messages.success(request, 'Invalid request method.')
        return redirect('users')
        

@user_passes_test(admin_check, login_url='home')
def products(request):
    products = Product.objects.all()
    # print(products)
    return render(request, 'dashboard/products.html', {'products':products})


@user_passes_test(admin_check, login_url='home')
def fetch_products(request):
   
    products = Product.objects.all()
    products_data = [
        {
            'id': product.id,
            'name': product.name,
            'image': product.image.url,
            'user': product.created_by.username,
            'price': product.price,
            'sale': product.is_sale if product.is_sale else 'unsale',
            'sale_price': product.sale_price if product.is_sale else 'Unsale',
            'category': product.category.name.split()[:2],
            'created_at': product.created_at,
            'updated_at': product.updated_at,
        }
        for product in products
    ]

    return JsonResponse({'products': products_data})


@user_passes_test(admin_check, login_url='home')
def create_product(request):
    if request.method == 'POST':

        form = CreateProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            
            messages.success(request, "Product added successfully!")  
            return redirect('create_product')  
        
        else:
            messages.error(request, "There was an error with the form. Please check the details and try again.")
 
    else:
        form = CreateProductForm()
    
    return render(request, 'dashboard/create_product.html', {'form': form})


# @user_passes_test(admin_check, login_url='home')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[0:3]
    if request.user.is_superuser:
 
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
    else:
        context = {
            'product':product,
            'related_products':related_products,
            'categories':categories,
            }
        return render(request, 'store/product_details.html', context)


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

    if request.method == 'POST':
        order_form = EditOrderForm(request.POST, instance=order)
        if order_form.is_valid():
            order_form.save()
            messages.success(request, 'Order status updated!.')
            return redirect('order', order_id)
        else:
            messages.success(request, 'There was an issue with the form, check details and try again!.')
            return redirect('order', order_id)
        
    return render(request, 'dashboard/order.html', 
                  {
                      'order':order, 
                    'order_items':order_items,
                    'order_form':order_form,
                   }
                   )

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order:
        order.delete()
        messages.success(request, f'Order "{order_id}" deleted successfully!.')
        return redirect('orders')
    else:
        messages.error(request, 'Order does not exist')
        return redirect('orders')


def pending_orders(request):
    
    pending_orders = Order.objects.filter(status__iexact='pending')
    return render(request, 'dashboard/pending_orders.html', {'orders':pending_orders})


def processing_orders(request):
    orders = Order.objects.filter(status__iexact='processing')

    return render(request, 'dashboard/processing_orders.html', {'orders':orders})

def shipped_orders(request):
    orders = Order.objects.filter(status__iexact='shipped')
    return render(request, 'dashboard/shipped_orders.html', {'orders':orders})

def delivered_orders(request):
    orders = Order.objects.filter(status__iexact='delivered')
    return render(request, 'dashboard/delivered_orders.html', {'orders':orders})

def cancelled_orders(request):
    orders = Order.objects.filter(status__iexact='cancelled')
    return render(request, 'dashboard/cancelled_orders.html', {'orders':orders})


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
            'email':order.email,
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
            'email':order.email,
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
def download_orders_excel(request):

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Order list'

    
    sheet.append(['Reference', 'Full Name', 'Email', 'Shipping Address', 'Amount Paid', 'Status', 'Date Ordered'])

    orders = Order.objects.all()

    for order in orders:
        naive_date_ordered = make_naive(order.date_ordered)
        sheet.append([order.reference, order.full_name, order.email, order.shipping_address, order.amount_paid, order.status, naive_date_ordered])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename"orders.xlsx"'
    workbook.save(response)
    return response



# def search_orders(request):
#     if request.method == 'GET':
#         search_term = request.GET.get('search_term')
#         results = Order.objects.filter(
#             Q(reference__icontains=search_term) | Q(email__icontains=search_term) | Q(date_ordered__icontains=search_term))

#         results_data = [
#         {
#             'id': order.id,
#             'reference': order.reference,
#             'user': order.user.username if order.user else 'Guest',
#             'email':order.email,
#             'amount_paid': order.amount_paid,
#             'status': order.get_status_display(),
#             'date_ordered': order.date_ordered.strftime('%Y-%m-%d %H:%M:%S'),
#             'status_choices': order.STATUS_CHOICES
#         }
#         for order in results
#     ]
#         return JsonResponse({'orders': results_data})
#     if not search_term:
#         return JsonResponse({'error': 'Search term is required.'}, status=400)


def search_orders(request):

    if request.GET:
        search_term = request.GET.get('search-input')
        
        if search_term:
            results = Order.objects.filter(
                Q(reference__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(date_ordered__icontains=search_term)
            )
            if not results:
                messages.error(request, f'Records not found for "{search_term}"')

                return redirect('search-order')
            else:
                return render(request, 'dashboard/search.html', {'results':results})
        else:
            messages.error(request, 'search term required')
            return redirect('search-order')
   
    return render(request, 'dashboard/search.html')


@user_passes_test(admin_check, login_url='home')
def category_list(request):
    categories = Category.objects.all()

    if categories:
        return render(request, 'dashboard/categories.html', {'categories':categories})
    else:
        messages.error(request, "You don't have catrgory yet, please add!")

        categories = "You don't have catrgory yet, please add!"
        return render(request, 'dashboard/categories.html', {'categories':categories})




@user_passes_test(admin_check, login_url='home')
def new_category(request):

    if request.method == 'POST':
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            name = category.name
            messages.success(request, f'Category "{name}" added successfully!')
            return redirect('new-category')
        
        else:
            messages.success(request, 'There was an error with the form. Please check the details and try again.')
            return redirect('new-category')
    else:
        form = NewCategoryForm()
    return render(request, 'dashboard/create_category.html', {'form':form})



@user_passes_test(admin_check, login_url='home')
def edit_category(request, category_id):
    category = Category.objects.filter(id=category_id).first()

    if category:
        if request.method == 'POST':

            edit_form = EditCategoryForm(request.POST, instance=category)
            if edit_form.is_valid():
                category = edit_form.save(commit=False)
                category.user = request.user
                category.save()
                name =  category.name
                messages.success(request, f"Category '{name}' updated successfully!")
                return redirect('edit-category', category.id)
            else:
                messages.success(request, 'There was an error with the form. Please check the details and try again.')
                return redirect('edit-category', category.id)
            
        else:
             edit_form = EditCategoryForm(instance=category)
        return render(request, 'dashboard/edit_category.html', {'edit_form':edit_form, 'category':category})
    
    else:
        messages.success(request, 'Category not found, try again.')
        return redirect('categories')

        
@user_passes_test(admin_check, login_url='home')
def delete_category(request, category_id):
    category = Category.objects.filter(id=category_id).first()

    if category:
        category.delete()
        messages.success(request, f"Category '{category.name}' Deleted successfully!")
        return redirect('categories')
    else:
        messages.success(request, 'There was an error deleting category, try again.')
        return redirect('categories')

@user_passes_test(admin_check, login_url='home')
def reports(request):
    return render(request, 'dashboard/reports.html', {})



@user_passes_test(admin_check, login_url='home')
def settings(request):

     return render(request, 'dashboard/settings.html', {})

