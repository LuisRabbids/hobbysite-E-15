from django.db import models
from django.urls import reverse
from user_management.models import Profile




# class for Article Category. Just a simple text field
# This works. Do not touch it
class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)  # max length is 255 characters

    description = models.TextField()

    class Meta:
        ordering = ['name']  # Sorts by name in ascending order

    def __str__(self):
        return self.name

# This works. Do not touch it. 
class Article (models.Model):
    # Title of the thing, max 255 characters
    title = models.CharField(max_length=255)

    # Connects it to the Article Category class
    category = models.ForeignKey(
        ArticleCategory, null=True, on_delete=models.SET_NULL)
    entry = models.TextField()

    # Gets made only once, when the model is created
    created_on = models.DateTimeField(auto_now_add=True)
    # Refreshes with any changes made.
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Sorted by the date it was created, in descending order, newest first.
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
# Comment
# Author - foreign key to Profile who created the comment, set to NULL when deleted


class Comment (models.Model):
    #TODO: THE REST OF THIS STUFF 

    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE, related_name= 'article_title')
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='profile_name')
    
    entry = models.TextField()
    # Gets made only once, when the model is created
    created_on = models.DateTimeField(auto_now_add=True)
    # Refreshes with any changes made.
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Sorted by the date it was created, in ascending order, oldest first.
        ordering = ['created_on']
