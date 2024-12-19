from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('404/', views.error_404, name='404'),
    path('password-reset/<str:username>/', views.password_reset, name='password-reset'),
    # path('forget_password/', views.forget_password, name='forget_password'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
]