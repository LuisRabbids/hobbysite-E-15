from django.urls import path
from . import views
from .views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView


urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/add/', ArticleCreateView.as_view(), name='add'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='edit'),
]

app_name = 'blog'