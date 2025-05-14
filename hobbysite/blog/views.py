
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Article, ArticleCategory, Comment
from blog.forms import CommentForm, ArticleForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/add.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user.profile
        article.save()
        return redirect('blog:article_detail', pk=article.pk)

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'pk': self.object.pk})

class ArticleListView(ListView):
    model = Article
    template_name = 'blog/blog_index.html'
    context_object_name = 'all_articles'

    def get_queryset(self):
        """Optimize the query with select_related for better performance."""
        return Article.objects.select_related('category', 'author').all()

    def get_context_data(self, **kwargs):
        """Inject additional context such as user-specific articles and categorized groups."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        user_articles = []
        other_articles = context['all_articles']

        if user.is_authenticated:
            user_profile = user.profile
            user_articles = other_articles.filter(author=user_profile)
            other_articles = other_articles.exclude(author=user_profile)

        categories = ArticleCategory.objects.all()
        category_groups = [
            (category, other_articles.filter(category=category).order_by('-created_on'))
            for category in categories if other_articles.filter(category=category).exists()
        ]

        context.update({
            'user_articles': user_articles,
            'category_groups': category_groups,
        })
        return context
    

class ArticleDetailView(DetailView, FormView):
    model = Article
    template_name = 'blog/blog_post.html'
    form_class = CommentForm
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.prefetch_related('comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        context['comments'] = article.comments.order_by('-created_on')
        context['related_articles'] = Article.objects.filter(author=article.author).exclude(pk=article.pk)[:2]
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        article = self.get_object()
        new_comment = form.save(commit=False)
        new_comment.article = article
        new_comment.author = self.request.user.profile
        new_comment.save()
        return redirect('blog:article_detail', pk=article.pk)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().post(request, *args, **kwargs)
        return redirect(reverse_lazy('login'))
    

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/add.html'

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        if self.request.user.profile != article.author:
            return redirect('blog:article_detail', pk=article.pk)
        return article

    def form_valid(self, form):
        article = form.save(commit=False)
        # Preserve the original author and created_on date
        article.author = self.object.author
        article.created_on = self.object.created_on
        article.save()
        return redirect('blog:article_detail', pk=article.pk)

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'pk': self.object.pk})