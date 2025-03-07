from django.db import models

# Create your models here.

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']  # Sorted by name in ascending order

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ArticleCategory, null=True, on_delete=models.SET_NULL)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_on = models.DateTimeField(auto_now=True)      # Updated on each save

    class Meta:
        ordering = ['-created_on']  # Sorted by creation date in descending order

    def __str__(self):
        return self.title
