from django.urls import path
from .views import forum_list, forum_detail

urlpatterns = [
    path('threads/', forum_list, name="forum-list"),
    path('thread/<int:id>', forum_detail, name='forum-detail')
]

app_name = 'forum'
