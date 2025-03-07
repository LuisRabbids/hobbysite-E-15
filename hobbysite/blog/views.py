from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from blog.models import Article


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'blog/blog_index.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'blog/blog_post.html', {'article': article})
