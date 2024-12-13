from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateProductForm,EditProductForm
from Store.models import Product
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def dashboard(request):
    return render(request, 'dashboard/index.html')



@login_required
def create_product(request):
    if request.method == 'POST':

        form = CreateProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            
            messages.success(request, "Product created successfully!")  # Feedback to the user
            
            # Redirect to the dashboard or a specific page for the product
            return redirect('dashboard')  
        else:
            messages.error(request, "There was an error with the form. Please check the details and try again.")
    
    else:
        form = CreateProductForm()
    
    return render(request, 'dashboard/create_product.html', {'form': form})


@login_required
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
    
    
    return render(request, 'dashboard/edit_product.html', {'edit_form': edit_form})




