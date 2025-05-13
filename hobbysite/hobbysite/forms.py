from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
      email = forms.EmailField(required=True) # Make email required

      class Meta(UserCreationForm.Meta):
          model = User
          fields = UserCreationForm.Meta.fields + ('email',)