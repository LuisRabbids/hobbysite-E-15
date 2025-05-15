from django.urls import path
from . import views

urlpatterns = [
    path('/list', views.commissions_list, name='commissions_list')
    path('/detail/<int:pk>', views.commission_detail, name='commission_detail')
    path('/add', views.commission_create, name='commission-create')
    path('/<int:pk>/edit', views.commission_update, name='commission-update')
]
