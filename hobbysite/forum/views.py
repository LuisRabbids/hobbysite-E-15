from django.shortcuts import render
from .models import Post, PostCategory


def forum_list(request):
    ctx = {
        "posts": Post.objects.all(),
        "categories": PostCategory.objects.all(),
    }
    return render(request, "forum/forum_list.html", ctx)


def forum_detail(request, slug):
    ctx = {'post': Post.objects.get(slug=slug)}
    return render(request, 'forum/forum_detail.html', ctx)
