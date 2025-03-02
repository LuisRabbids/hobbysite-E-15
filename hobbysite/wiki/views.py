from django.shortcuts import render, get_object_or_404
from .models import Article
# Create your views here.

def article_list(request):
    articles = Article.objects.all()  # Will be sorted by '-created_on' as per Meta
    return render(request, 'wiki/article_list.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'wiki/article_detail.html', {'article': article})
