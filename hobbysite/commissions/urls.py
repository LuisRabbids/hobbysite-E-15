from django.urls import path
from .views import views

urlpatterns = [
    path('/commissions/list', views.commissions_list, name='commissions_list'),
    path('/commissions/detail/1', views.commission_detail, name='commission_detail'),
    path('/commissions/create', views.commission_create, name='commission-create'),
    path('/commissions/update', views.commission_update, name='commission-update')
]
