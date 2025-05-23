from django.shortcuts import render,redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

import requests
import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ProductSerializer, CategorySerializer

from .models import Category, Product, Collection, CollectionItem
from .forms import ProductForm





def home(request):
    trending_products = trending()
    featured_products = featured_product()
    best_selling_products = best_selling()

    categories = Category.objects.all()
    collections = Collection.objects.all()
    # products_category = product_category(request, id=pk)
    context = {
        'trending_products':trending_products,
        # 'products_category':products_category,
        'featured_products':featured_products,
        'best_selling_products':best_selling_products,
        'categories':categories,
        'collections':collections,
    }
    return render(request, 'store/index.html', context)


def collection_list(request):
    collections = Collection.objects.all()
    return render(request, 'store/collection_list.html', {'collections':collections})

def collection_detail(request, slug):
     collection = get_object_or_404(Collection, slug=slug)
     collection_items = CollectionItem.objects.filter(collection=collection)
     return render(request, 'store/collection_detail.html', {'collection':collection, 'collection_items':collection_items})


def best_selling():
    best_selling = Product.objects.filter(is_best_seller=True)
    return best_selling

def trending():
    trending_products = Product.objects.filter(is_trending=True)
    trending_products[1:12]
    return trending_products
    
def update_featured_product(request, pk):
    if request.method == 'POST':
        # is_featured = request.POST['is_featured']
        try:
            product = get_object_or_404(Product, id=pk)
        except product.DoesNotExist:
            messages.error(request, 'Product not found')
            return redirect('/')
        product.is_featured = True
        product.save()
        return Response(product)

def featured_product():
    featured_products = Product.objects.filter(is_featured=True)
    return featured_products         

def product_category(request, pk):
    if request.method == 'GET':
        
        try:
            category = get_object_or_404(Category, id=pk)
        except category.DoesNotExist:
            return Response({'error': 'category not Found'}, status=status.HTTP_204_NO_CONTENT)
        
        products_category = get_list_or_404(Product, category=category)
        return render(request, 'store/products_category.html', {'products_category':products_category})


def shop_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    first_ten_products = Product.objects.all()[0:6]
    second_ten_products = Product.objects.all()[6:12]
    third_ten_products = Product.objects.all()[12:18]
    fourth_ten_products = Product.objects.all()[18:24]
    
   
    trending_products = Product.objects.filter(is_trending=True)
    best_seller_products = Product.objects.filter(is_best_seller=True)
    featured_products = Product.objects.filter(is_featured=True)

    context = {
        'categories':categories,
        'products':products,
        'trending_products':trending_products,
        'best_seller_products':best_seller_products,
        'featured_products':featured_products,
        'first_ten_products':first_ten_products,
        'second_ten_products':second_ten_products,
        'third_ten_products':third_ten_products,
        'fourth_ten_products':fourth_ten_products,
    }
    return render(request, 'store/shop.html', context)

def category_detail(request, category):
    categories = Category.objects.all()

    category = get_object_or_404(Category, name=category)
    try:

        category_products = Product.objects.filter(category=category)

    except Product.objects.filter(category=category).DoesNotExist():
        messages.success(request, 'No product found for this category' + category)
        return render(request, 'store/category_detail.html')
    return render(request, 'store/category_detail.html', {'category_products':category_products, 'categories':categories, 'category':category})

def search(request):
    if request.GET:
        search_term = request.GET.get('search-term')
        search_result = Product.objects.filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term)) 
           
        return render(request, 'store/search.html', {'search_result':search_result, 'search_term':search_term})
    
    return render(request, 'store/search.html', {})

def search_shop(request):
    if request.method == 'GET':
        search_term = request.GET.get('search_term', '')
        search_result = Product.objects.filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term))  
        search_data = [
            {
                'id':product.id, 
                'name':product.name, 
                'image':product.image.url,
                'description':product.description, 
                'price':product.price, 
                'is_sale':product.is_sale, 
                'sale_price':product.sale_price
            }
            for product in search_result
        ]
        print(search_data)
        return JsonResponse({
            'search_result':search_data, 
            'search_term':search_term
            })

# def product_details(request, product_id):
#     categories = Category.objects.all()

#     product = get_object_or_404(Product, id=product_id)
#     related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[0:3]
#     if request.user.is_superuser:

#         return render(request, 'dashboard/products.html', {'products':products})
#     else:

#         context = {
#             'product':product,
#             'related_products':related_products,
#             'categories':categories,
#             }
#         return render(request, 'store/product_details.html', context)













@api_view(['POST'])
def new_product(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def get_product(request, pk):
    try:
        product = get_object_or_404(Product, id=pk)
    except product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def new_category(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def get_category(request, pk):
    try:
        category = get_object_or_404(Category, id=pk)
    except category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
