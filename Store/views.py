from django.shortcuts import render,redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ProductSerializer, CategorySerializer
from django.http import HttpResponse
from .models import Category, Product, Collection
from .forms import ProductForm




def home(request):
    trending_products = trending(request)
    featured_products = featured_product()
    categories = Category.objects.all()
    # products_category = product_category(request, id=pk)
    context = {
        'trending_products':trending_products,
        # 'products_category':products_category,
        'featured_products':featured_products,
        'categories':categories,
    }
    return render(request, 'store/index.html', context)

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
    
def trending(request):
    if request.method == 'GET':
        products = Product.objects.all()
        trending_products = products.reverse()
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
    featured_products.reverse
    return featured_products         

def product_category(request, pk):
    if request.method == 'GET':
        
        try:
            category = get_object_or_404(Category, id=pk)
        except category.DoesNotExist:
            return Response({'error': 'category not Found'}, status=status.HTTP_204_NO_CONTENT)
        
        products_category = get_list_or_404(Product, category=category)
        return render(request, 'store/products_category.html', {'products_category':products_category})
# shop logic

def shop_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories':categories,
        'products':products,
    }
    # categories
    # trending products
    # popular prodycts
    # new arrivals 
    # best sellers
    # discounted or on-sale products
    # recommed products
    # featured products

    return render(request, 'store/shop.html', context)