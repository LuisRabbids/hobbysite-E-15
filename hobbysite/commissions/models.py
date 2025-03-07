from django.db import models

class CommissionCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']  # Sorted by category name in ascending order

    def __str__(self):
        return self.name

class Commission(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        CommissionCategory,
        null=True,
        on_delete=models.SET_NULL)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Only set on creation

    class Meta:
        ordering = ['-created_on']  # Sorted by commission creation date in descending order

    def __str__(self):
        return self.title