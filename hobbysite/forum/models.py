from django.db import models

# Create your models here.
class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']  # categories sorted by name in ascending order