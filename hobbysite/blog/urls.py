from django.urls import path
from . import views
from .views import view_function, CreateArticle, EditArticle, ArticlesListView, ArticleDetailView


urlpatterns = [
    path('articles/', ArticlesListView.as_view(), name='article_list'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('accounts/login/', view_function, name= 'login'),
    path('articles/add', CreateArticle.as_view(), name ='add'),
    path('article/<int:pk>/edit', EditArticle.as_view(), name='edit')
]

app_name = 'blog'