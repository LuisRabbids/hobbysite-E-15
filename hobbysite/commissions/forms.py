from django import forms
from .models import Commission, Comment, Job, JobApplication

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'author', 'description', 'status', 'people_required']
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commission', 'entry',]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['commission', 'role', 'manpower_required', 'status',]

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['job', 'applicant', 'status']