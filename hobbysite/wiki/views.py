# wiki/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm, CommentForm
from django.db.models import Q, Prefetch # MODIFIED: Added Prefetch here

class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_articles = Article.objects.select_related('category', 'author').all()
        user_articles = []

        current_user_pk = None
        if self.request.user.is_authenticated:
            current_user_pk = self.request.user.pk
            user_articles = all_articles.filter(author=self.request.user)
            all_articles = all_articles.exclude(author=self.request.user)


        # Prepare the queryset for prefetching articles for categories
        # Exclude articles by the current user if authenticated
        articles_for_categories_qs = Article.objects.all()
        if current_user_pk:
            articles_for_categories_qs = articles_for_categories_qs.exclude(author_id=current_user_pk)

        categories_with_articles = ArticleCategory.objects.prefetch_related(
            Prefetch( # MODIFIED: Changed from models.Prefetch to Prefetch
                'articles',
                queryset=articles_for_categories_qs.select_related('author')
            )
        ).distinct()


        context['user_articles'] = user_articles
        context['categories_with_articles'] = categories_with_articles
        context['create_article_url'] = reverse_lazy('wiki:article_create')
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        if article.category:
            related_articles = Article.objects.filter(category=article.category)\
                                            .exclude(pk=article.pk)\
                                            .order_by('?')[:2]
            context['related_articles'] = related_articles
        else:
            context['related_articles'] = Article.objects.none()

        context['comments'] = article.comments.all().order_by('-created_on')

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        context['back_to_list_url'] = reverse_lazy('wiki:article_list')
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user
            comment.save()
            return redirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = "Create New Wiki Article"
        return context

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_form.html'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Update: {self.object.title}"
        return context