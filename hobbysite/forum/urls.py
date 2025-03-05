from django.urls import path
from .views import forum_list, forum_detail

urlpatterns = [
    path('', forum_list, name="forum-list"),
    path('<int:id>', forum_detail, name='forum-detail')
]

app_name = 'forum'