# wiki/models.py
from django.db import models
from user_management.models import Profile

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Article Categories" 
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory, null=True, on_delete=models.SET_NULL, related_name="articles"
    )
    # settings.AUTH_USER_MODEL is preferred over directly importing User
    # in case you have a custom user model in the future.
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="wiki_articles"
    )
    entry = models.TextField()
    header_image = models.ImageField(
        upload_to='images/wiki_images/', null=True, blank=True 
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('wiki:article_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='wiki_comments')
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on'] 

    def __str__(self):
        return f'Comment by {self.author.user.username} on {self.article.title}'
