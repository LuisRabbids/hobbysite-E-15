from django import forms
from .models import Commission, Comment, Job, JobApplication

class CommissionForm(forms.Form):
    class Meta:
        model = Commission()
        fields = ['title', 'author', 'description', 'status', 'people_required', 'created_on', 'updated_on']
    