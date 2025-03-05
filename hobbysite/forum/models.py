from datetime import datetime
from django.db import models

# Create your models here.
class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']  # categories sorted by name in ascending order


class Post(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        PostCategory,
        on_delete = models.SET_NULL,
        null = True
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']