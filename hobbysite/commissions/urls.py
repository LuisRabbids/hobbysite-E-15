from django.urls import path
from . import views

app_name = 'commissions'

urlpatterns = [
    path('list/', views.commissions_list, name='commissions_list'),
    path('add/', views.commission_create, name='commission_create'), # Changed name for consistency
    path('detail/<int:pk>/', views.commission_detail, name='commission_detail'),
    path('<int:pk>/edit/', views.commission_update, name='commission_update'),
]