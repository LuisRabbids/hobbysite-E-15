from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required  # For function-based views if needed
from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm, CommentForm
from django.db.models import Prefetch


class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'
    context_object_name = 'articles'  # Not directly used—kept for completeness

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Base queryset for all articles (with related objects for performance)
        all_articles_qs = Article.objects.select_related('author', 'category')

        # --- 1.  Gather the logged-in user’s own articles  -------------------
        user_articles = Article.objects.none()
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
            user_articles = all_articles_qs.filter(author=user_profile)
            # Remove them from the queryset that will populate “All Articles”
            all_articles_qs = all_articles_qs.exclude(author=user_profile)

        # --- 2.  Prefetch the remaining articles into their categories -------
        categories_with_articles = (
            ArticleCategory.objects
            .prefetch_related(
                Prefetch('articles', queryset=all_articles_qs)
            )
            .order_by('name')
        )

        # --- 3.  Add everything to the template context  ---------------------
        context.update({
            "user_articles": user_articles,
            "categories_with_articles": categories_with_articles,
            "create_article_url": reverse_lazy("wiki:article_create"),
        })
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        if article.category:
            context['related_articles'] = (
                Article.objects
                .filter(category=article.category)
                .exclude(pk=article.pk)
                .order_by('?')[:2]
            )
        else:
            context['related_articles'] = Article.objects.none()

        context['comments'] = article.comments.all()

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
            comment.author = request.user.profile
            comment.save()
            return redirect(self.object.get_absolute_url())

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
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
        return self.request.user.profile == article.author

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Update: {self.object.title}"
        return context
