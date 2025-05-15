# wiki/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required # For function-based views if needed
from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm, CommentForm
from django.db.models import Q, Prefetch

# wiki/views.py

# ... (other imports and views) ...

class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'
    context_object_name = 'articles' # This isn't directly used if you rely on categories_with_articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Always fetch all articles for category grouping
        all_articles_for_grouping_qs = Article.objects.select_related('author', 'category').all()

        categories_with_articles = ArticleCategory.objects.prefetch_related(
            Prefetch(
                'articles', # Assumes Article.category has related_name='articles' or you use article_set
                queryset=all_articles_for_grouping_qs
            )
        ).distinct().order_by('name') # Order categories by name

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
                                            .order_by('?')[:2] # Get 2 random ones
            context['related_articles'] = related_articles
        else:
            context['related_articles'] = Article.objects.none()

        context['comments'] = article.comments.all() # .order_by('-created_on') is handled by model Meta

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        context['back_to_list_url'] = reverse_lazy('wiki:article_list')
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') # Or handle as an error

        self.object = self.get_object() # Get the article object
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user.profile
            comment.save()
            return redirect(self.object.get_absolute_url()) # Redirect back to the article detail page
        else:
            # If form is not valid, re-render the page with the form and errors
            context = self.get_context_data() # Get existing context
            context['comment_form'] = form # Overwrite with the form containing errors
            return self.render_to_response(context)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile # Set author to logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the detail view of the created article
        return self.object.get_absolute_url() # Assumes get_absolute_url is defined on Article model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = "Create New Wiki Article"
        return context

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_form.html'

    def test_func(self):
        # Check if the logged-in user is the author of the article
        article = self.get_object()
        return self.request.user.profile == article.author

    def get_success_url(self):
        return self.object.get_absolute_url() # Assumes get_absolute_url is defined on Article model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Update: {self.object.title}"
        return context