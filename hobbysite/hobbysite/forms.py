from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_management.models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    display_name = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            display_name = self.cleaned_data.get(
                'display_name') or user.username
            Profile.objects.create(user=user, display_name=display_name)
        return user
