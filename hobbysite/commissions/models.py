from django.db import models
from user_management.models import Profile

class Commission(models.Model):
    commission_status = [ #creates list for commission status
        ('o','Open'),
        ('f','Full'),
        ('c','Completed'),
        ('d','Discontinued'),
    ]

    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.CASCADE
    )
    description = models.TextField()
    status = models.CharField(max_length=1, choices=commission_status, default='o')
    people_required = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)  # Only set on creation
    updated_on = models.DateTimeField(auto_now=True) # Updates with modification date

    class Meta:
        ordering = ['created_on']  # Sorted by commission creation date in ascending order

    def __str__(self):
        return self.title

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

class Job(models.Model):
    job_status = [ #creates list for job status
        ('o','Open'),
        ('f','Full'),
    ]

    commission = models.ForeignKey(
        Commission,
        null=True,
        on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    status = models.CharField(max_length=1, choices=job_status, default='o')

    class Meta:
        ordering = ['-status', 'manpower_required', 'role']  # Sorted by status and manpower (descending), then role (ascending)

    def __str__(self):
        return self.name

class JobApplication(models.Model):
    application_status = [ #creates list for job application status
        ('p','Pending'),
        ('a','Accepted'),
        ('r','Rejected'),
    ]

    job = models.ForeignKey(
        Job,
        null=True,
        on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=application_status, default='p')
    applied_on = models.DateTimeField(auto_now_add=True)  # Only set on creation
    
    class Meta:
        ordering = ['-status', '-applied_on']  # Sorted by status and applied on date in descending order

    def __str__(self):
        return self.name
