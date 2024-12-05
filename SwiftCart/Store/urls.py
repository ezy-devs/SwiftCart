from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('new-product/', views.new_product, name='new-product'),
    path('products/', views.products, name='products'),
    path('get-product/<uuid:pk>/', views.get_product, name='get-product'),
    path('new-category/', views.new_category, name='new-category'),
    path('get-category/<int:pk>/', views.get_category, name='get-category'),
    path('categories/', views.categories, name='categories'),
    path('products-category/<int:pk>/', views.product_category, name='products-category'),
    path('update-featured-product/<uuid:pk>/', views.update_featured_product, name='update-featured-product'),
    path('shop/', views.shop, name='shop'),
]