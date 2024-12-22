from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('new-product/', views.new_product, name='new-product'),
    path('products/', views.products, name='products'),
    path('get-product/<uuid:pk>/', views.get_product, name='get-product'),
    path('new-category/', views.new_category, name='new-category'),
    path('get-category/<int:pk>/', views.get_category, name='get-category'),
    path('category_detail/<str:category>/', views.category_detail, name='category_detail'),
    path('categories/', views.categories, name='categories'),
    path('products-category/<int:pk>/', views.product_category, name='products-category'),
    path('update-featured-product/<uuid:pk>/', views.update_featured_product, name='update-featured-product'),
    path('product/<uuid:product_id>/', views.product_details, name='product'),
    path('shop/', views.shop_page, name='shop'),
    path('search/', views.search, name='search'),
    # path('search_shop/', views.search_shop, name='search_shop'),
    path('search_shop/', views.search_shop, name='search_shop'),
    path('collection/<slug:slug>/', views.collection_detail, name='collection_detail'),
    path('collections/', views.collection_list, name='collections'),
]