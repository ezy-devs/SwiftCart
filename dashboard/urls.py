from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('add_new_product/', views.add_new_product, name='add_new_product'),
    path('create_product/', views.create_product, name='create_product'),
    path('edit_product/<uuid:product_id>/', views.edit_product, name='edit_product'),
]