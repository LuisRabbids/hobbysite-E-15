from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Article, ArticleCategory
from .forms import CommentForm, ArticleForm
from django.contrib.auth.decorators import login_required
from .models import Profile


def article_list(request):
    user = request.user
    all_articles = Article.objects.select_related('category', 'author').all()
    
    user_articles = []
    other_articles = all_articles

    if user.is_authenticated:
        user_profile = user.profile
        user_articles = all_articles.filter(author=user_profile)
        other_articles = all_articles.exclude(author=user_profile)

    categories = ArticleCategory.objects.all()
    category_groups = []
    for category in categories:
        articles_in_category = other_articles.filter(category=category).order_by('-created_on')
        if articles_in_category.exists():
            category_groups.append((category, articles_in_category))

    context = {
        'user_articles': user_articles,
        'category_groups': category_groups,
    }
    return render(request, 'blog/article_list.html', context)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.order_by('-created_on')
    related_articles = Article.objects.filter(author=article.author).exclude(pk=pk)[:2]

    form = CommentForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user.profile
            new_comment.save()
            return redirect('blog:article-detail', pk=article.pk)

    context = {
        'article': article,
        'comments': comments,
        'related_articles': related_articles,
        'form': form,
    }
    return render(request, 'blog/article_detail.html', context)



@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.profile
            article.save()
            return redirect('blog:article-detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_create.html', {'form': form})


@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    # Prevent non-authors from editing
    if request.user.profile != article.author:
        return redirect('blog:article-detail', pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            updated_article = form.save(commit=False)
            # preserve the original author and created_on
            updated_article.author = article.author
            updated_article.created_on = article.created_on
            updated_article.save()
            return redirect('blog:article-detail', pk=pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_update.html', {'form': form, 'article': article})