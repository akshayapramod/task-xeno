from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='product_list'),
    path('home', views.user_home, name='home'),
    path('login_view/', views.login_view, name='login_view'),
    path('products/', views.product_list, name='products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_complete/', views.order_complete, name='order_complete'),
]
