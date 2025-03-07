from django.urls import path
from .views import index

urlpatterns = [
    path('commissions/', views.commissions_list, name='commissions_list')
    path('commission/<int:commission_id>/', views.commission_detail, name='commission_detail')
]