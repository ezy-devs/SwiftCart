from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('de-activate-user/<int:user_id>', views.de_activate_user, name='de-activate-user'),
    path('create_product/', views.create_product, name='create_product'),
    path('products/', views.products, name='products'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:order_id>/', views.order, name='order'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
    path('edit_product/<uuid:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product', views.delete_product, name='delete_product'),
]