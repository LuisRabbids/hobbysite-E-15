from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm # For basic registration
from django.shortcuts import redirect # For registration
from django.contrib import messages # For registration messages

from django.shortcuts import render, redirect
from .forms import RegistrationForm # Import your new form

def homepage(request):
    context = {} # Add any data you want to pass to the template here
    return render(request, 'homepage.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # Using a basic form for now
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') # Assumes 'login' is a named URL
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def homepage(request):
      # ... (existing homepage view) ...
      return render(request, 'homepage.html')

def register(request):
      if request.method == 'POST':
          form = RegistrationForm(request.POST)
          if form.is_valid():
              form.save()
              username = form.cleaned_data.get('username')
              messages.success(request, f'Account created for {username}! You can now log in.')
              return redirect('login') # Redirect to login page after successful registration
      else:
          form = RegistrationForm()
      return render(request, 'registration/register.html', {'form': form})