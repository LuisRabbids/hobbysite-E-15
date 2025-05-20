from django.db import models
from django.conf import settings # Recommended for ForeignKey to User/Profile
from user_management.models import Profile # Assuming this is your Profile model
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField, Sum, Count, F, Q

class Commission(models.Model):
    OPEN = 'O'
    FULL = 'F'
    COMPLETED = 'C'
    DISCONTINUED = 'D'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (FULL, 'Full'),
        (COMPLETED, 'Completed'),
        (DISCONTINUED, 'Discontinued'),
    ]

    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='commissions_authored'
    )
    description = models.TextField()
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=OPEN
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on'] # Default sort: oldest first as per requirement

    def __str__(self):
        return self.title

    def get_total_manpower_required(self):
        return self.jobs.aggregate(total_manpower=Sum('manpower_required'))['total_manpower'] or 0

    def get_accepted_applicants_count(self):
        return JobApplication.objects.filter(job__commission=self, status=JobApplication.ACCEPTED).count()

    def get_open_manpower(self):
        total_manpower = self.get_total_manpower_required()
        accepted_count = self.get_accepted_applicants_count()
        return total_manpower - accepted_count

class Job(models.Model):
    OPEN = 'O'
    FULL = 'F'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (FULL, 'Full'),
    ]

    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField() # Whole number
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=OPEN
    )

    class Meta:
        
        ordering = ['-status', '-manpower_required', 'role']

    def __str__(self):
        return f"{self.role} for {self.commission.title}"

    def get_accepted_applicants_count(self):
        return self.applications.filter(status=JobApplication.ACCEPTED).count()

    def is_full(self):
        return self.get_accepted_applicants_count() >= self.manpower_required

    def update_status_if_full(self):
        if self.is_full() and self.status == Job.OPEN:
            self.status = Job.FULL
            self.save(update_fields=['status'])
            return True
        return False


class JobApplication(models.Model):
    PENDING = '1' # Values chosen for correct sorting
    ACCEPTED = '2'
    REJECTED = '3'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Sorted by status (Pending > Accepted > Rejected), then Applied On (desc)
        ordering = ['status', '-applied_on']
        unique_together = ('job', 'applicant') # A user can only apply once to a specific job

    def __str__(self):
        return f"Application by {self.applicant} for {self.job.role}"