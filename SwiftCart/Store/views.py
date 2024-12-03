from django.shortcuts import render,redirect
from .serializers import ProductSerializer

from .models import Category, Product, Collection


def home(request):
    return render(request, 'store/index.html')


def add_product(request):
    pass