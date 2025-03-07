from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.commissions_list, name='commissions_list'),
    path('detail/<int:commission_id>',views.commission_detail, name='commission_detail'),
]
