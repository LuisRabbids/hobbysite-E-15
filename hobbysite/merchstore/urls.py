from django.urls import path
from . import views

app_name = 'merchstore'

urlpatterns = [
    path('items/', views.ProductListView.as_view(), name='product-list'),
    path('item/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('item/add/', views.ProductCreateView.as_view(), name='product-add'),
    path('item/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product-edit'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('transactions/', views.SellerTransactionListView.as_view(), name='transactions'),
]
