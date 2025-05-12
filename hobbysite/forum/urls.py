from django.urls import path
from . import views


urlpatterns = [
    path('threads/', views.thread_list, name='thread-list'),
    path('thread/<int:pk>/', views.thread_detail, name='thread-detail'),
    path('thread/add/', views.thread_create, name='thread-create'),
    path('thread/<int:pk>/edit/', views.thread_edit, name='thread-edit'),
]


app_name = 'forum'
