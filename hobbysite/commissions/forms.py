from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Job, JobApplication # NO Comment model here

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'status': forms.Select(choices=Commission.STATUS_CHOICES),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['role', 'manpower_required', 'status']
        widgets = {
            'status': forms.Select(choices=Job.STATUS_CHOICES),
        }

JobFormSet = inlineformset_factory(
    Commission,
    Job,
    form=JobForm,
    extra=1,
    can_delete=True,
    fk_name='commission'
)

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []

class JobApplicationUpdateForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status']
        widgets = {
            # Ensure choices are dynamically pulled if they can change,
            # or ensure they are correct here. STATUS_CHOICES on model is fine.
            'status': forms.Select(choices=JobApplication.STATUS_CHOICES),
        }