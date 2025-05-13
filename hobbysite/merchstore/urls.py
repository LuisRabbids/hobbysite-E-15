from django.urls import path
from . import views


app_name = 'merchstore'

urlpatterns = [
    path('items/', views.product_list, name='product-list'),
    path('item/<int:pk>/', views.product_detail, name='product-detail'),
    path('item/add/', views.product_create, name='product-add'),
    path('item/<int:pk>/edit/', views.product_edit, name='product-edit'),
    path('cart/', views.cart, name='cart'),
    path('transactions/', views.transactions, name='transactions'),
]
