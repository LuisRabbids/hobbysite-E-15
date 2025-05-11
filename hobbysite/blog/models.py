from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# class for Article Category. Just a simple text field
class ArticleCategory(models.Model):
    name = models.CharField(max_length=255) #max length is 255 characters
    
    description = models.TextField()

    class Meta:
        ordering = ['name'] # Sorts by name in ascending order

    def __str__(self):
        return self.name


class Article (models.Model):
    title = models.CharField(max_length=255) # Title of the thing, max 255 characters

    category = models.ForeignKey(ArticleCategory, null =True, on_delete=models.SET_NULL) # Connects it to the Article Category class
    entry = models.TextField()

    headerImage = models.ImageField(upload_to='blog_header_images/', null= True, blank = True, default = None) # Image for the header.
    #TODO All the other associated stuff. Go to settings and stuff.
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blog_articles')
    

    created_on = models.DateTimeField(auto_now_add = True) # Gets made only once, when the model is created
    last_updated = models.DateTimeField(auto_now= True) # Refreshes with any changes made.

    class Meta:
        ordering = ['-created_on'] # Sorted by the date it was created, in descending order, newest first. 
        
    def __str__(self):
        return self.title
    
class Comment (models.Model):
    #TODO: THE REST OF THIS STUFF 

    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE, related_name= 'comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blog_comments')
    
    entry = models.TextField()
    # Gets made only once, when the model is created
    created_on = models.DateTimeField(auto_now_add=True)
    # Refreshes with any changes made.
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Sorted by the date it was created, in ascending order, oldest first.
        ordering = ['created_on']

    