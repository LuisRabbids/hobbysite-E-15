from django import forms
from .models import Commission, Comment, Job, JobApplication

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission()
        fields = ['title', 'author', 'description', 'status', 'people_required', 'created_on', 'updated_on']
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment()
        fields = ['commission', 'entry', 'created_on', 'updated_on']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job()
        fields = ['commission', 'role', 'manpower_required', 'status']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication()
        fields = ['job', 'applicant', 'status', 'applied_on']