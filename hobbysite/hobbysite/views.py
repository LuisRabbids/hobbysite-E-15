from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm # For basic registration
from django.shortcuts import redirect # For registration
from django.contrib import messages # For registration messages

def homepage(request):
    # You can add context here if needed later, e.g., links to apps
    context = {} # Add any data you want to pass to the template here
    return render(request, 'homepage.html', context)

# If you are adding the registration view here:
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