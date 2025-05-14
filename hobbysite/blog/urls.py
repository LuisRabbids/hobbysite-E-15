from django.urls import path
from . import views


urlpatterns = [
    path('articles/', views.article_list, name='article-list'),
    path('article/<int:pk>/', views.article_detail, name='article-detail'),
    path('articles/add/', views.article_create, name='article-create'),
    path('article/<int:pk>/edit/', views.article_update, name='article-update'),
]

app_name = 'blog'