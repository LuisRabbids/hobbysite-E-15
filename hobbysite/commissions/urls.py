from django.urls import path
from .views import index
urlpatterns = [
    path('', index, name='index'),
    path('commissions/', views.commissions_list, name='commissions_list')
]