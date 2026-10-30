from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('register/', views.register, name='register'),
    path('login/', views.ShopLoginView.as_view(), name='login'),
    path('logout/', views.ShopLogoutView.as_view(), name='logout'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]
