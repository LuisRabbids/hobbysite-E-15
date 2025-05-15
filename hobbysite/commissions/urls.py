from django.urls import path
from .views import views

urlpatterns = [
    path('/list', views.commissions_list, name='commissions_list')
    path('/<int:pk>/detail', views.commission_detail, name='commission_detail')
    path('/create', views.commission_create, name='commission-create')
    path('/<int:pk>/update', views.commission_update, name='commission-update')
]