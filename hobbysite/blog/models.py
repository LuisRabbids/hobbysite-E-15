from django.db import models


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

    created_on = models.DateTimeField(auto_now_add = True) # Gets made only once, when the model is created
    last_updated = models.DateTimeField(auto_now= True) # Refreshes with any changes made.

    class Meta:
        ordering = ['-created_on'] # Sorted by the date it was created, in descending order, newest first. 
        
    def __str__(self):
        return self.title
    