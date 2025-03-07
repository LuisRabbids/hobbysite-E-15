from django.db import models

class Comment(models.Model):
    commission = models.ForeignKey(
        Commission,
        null=True,
        on_delete=models.CASCADE)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Only set on creation
    updated_on = models.DateTimeField(auto_now=True) # Updates with modification date

    class Meta:
        ordering = ['-created_on']  # Sorted by comment creation date in descending order

    def __str__(self):
        return self.name

class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)  # Only set on creation
    updated_on = models.DateTimeField(auto_now=True) # Updates with modification date

    class Meta:
        ordering = ['created_on']  # Sorted by commission creation date in ascending order

    def __str__(self):
        return self.title