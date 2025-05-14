from django.urls import path
from .views import commissions_list, commission_detail

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls'))
    path('/commissions/list', views.commissions_list, name='commissions_list')
    path('/commissions/detail/1', views.commission_detail, name='commission_detail')
]