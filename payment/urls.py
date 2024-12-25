from django.urls import path
from . import views

urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('verify-payment/', views.verify_payment, name='verify-payment'),
    path('webhook/', views.paystack_webhook, name='paystack_webhook'),
    path('checkout', views.checkout, name='checkout'),
    path('shipping_info/', views.shipping_info, name='shipping_info'),
    path('billing_info', views.billing_info, name='billing_info'),
    path('process_order', views.process_order, name='process_order'),
]