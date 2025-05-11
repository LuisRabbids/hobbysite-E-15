from django.urls import path
from . import views
from .views import view_function, CreateArticle, EditArticle

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('accounts/login/', view_function, name= 'login'),
    path('add', CreateArticle.as_view(), name ='add'),
    path('article/<int:article_id>/edit', EditArticle.as_view(), name='edit')
]

app_name = 'blog'