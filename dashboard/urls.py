from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('new_user/', views.new_user, name='new_user'),
    path('view_profile/<str:username>', views.view_profile, name='view_profile'),
    path('download_users_excel/', views.download_users_excel, name='download_users_excel'),
    path('download_orders_excel/', views.download_orders_excel, name='download_orders_excel'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('deactivate-user/<int:user_id>', views.deactivate_user, name='deactivate-user'),
    path('activate-user/<int:user_id>', views.activate_user, name='activate-user'),
    path('create_product/', views.create_product, name='create_product'),
    path('products/', views.products, name='products'),
    path('product/<uuid:product_id>', views.edit_product, name='product'),
    path('fetch_products', views.fetch_products, name='fetch_products'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:order_id>/', views.order, name='order'),
    path('reports/', views.reports, name='reports'),
    path('update_order/', views.update_order, name='update_order'),
    path('get_recent_orders/', views.get_recent_orders, name='get_recent_orders'),
    path('search-order/', views.search_orders, name='search-order'),
    path('all-search/', views.search, name='all-search'),
    path('settings/', views.settings, name='settings'),
    path('delete_product', views.delete_product, name='delete_product'),
    path('new-category', views.new_category, name='new-category'),
    path('delete-category/<int:category_id>', views.delete_category, name='delete-category'),
    path('edit-category/<int:category_id>', views.edit_category, name='edit-category'),
    path('categories', views.category_list, name='categories'),
]