from django.db import models


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.IntegerField(default=1)
    created_on = models.DateTimeField(
        auto_now_add=True)  # Only set on creation
    # Updates with modification date
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # Sorted by commission creation date in ascending order
        ordering = ['created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    commission = models.ForeignKey(
        Commission,
        null=True,
        on_delete=models.CASCADE)
    entry = models.TextField()
    created_on = models.DateTimeField(
        auto_now_add=True)  # Only set on creation
    # Updates with modification date
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # Sorted by comment creation date in descending order
        ordering = ['-created_on']

    def __str__(self):
        return self.name
