from django.urls import path
from . import views

urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('update_shipping_info/', views.update_shipping_info, name='update_shipping_info'),
]