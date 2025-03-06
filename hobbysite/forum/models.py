from django.db import models
from django.utils.text import slugify


class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # categories sorted by name in ascending order


class Post(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        PostCategory,
        on_delete=models.SET_NULL,
        null=True
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def __str__(self):
        return f"{self.title} ({self.category.name if self.category else 'No Category'})"

    class Meta:
        ordering = ['-created_on']  # posts sorted by date it was created, in descending order
