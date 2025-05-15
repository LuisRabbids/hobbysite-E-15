# wiki/urls.py
from django.urls import path
from . import views

app_name = 'wiki' 

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'), 
    path('article/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/update/', views.ArticleUpdateView.as_view(), name='article_update'),
  
]