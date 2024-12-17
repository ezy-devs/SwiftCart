from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_summary, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('fetch_cart', views.fetch_cart, name='fetch_cart'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
]