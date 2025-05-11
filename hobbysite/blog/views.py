from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from blog.models import Article
from django.views.generic import DetailView, CreateView, UpdateView
from .forms import ArticleForm


def article_list(request):
    articles = Article.objects.all() 
    return render(request, 'blog/blog_index.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'blog/blog_post.html', {'article': article})


class CreateArticle(CreateView):
    #Thing that allows users to make new recipies
    model = Article
    template_name = "blog/add.html"
    form_class = ArticleForm
    def get_success_url(self):
        return reverse_lazy('blog:article_list')
    
class EditArticle(UpdateView):
    model = Article
    template_name ="blog/add.html"
    form_class = ArticleForm

    def get_success_url(self):
        return reverse_lazy('blog:article_list')

@login_required
def view_function(request):
    return render(request, "blog/registration.html")