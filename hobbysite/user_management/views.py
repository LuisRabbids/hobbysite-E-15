from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm


@login_required
def update_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            form = ProfileUpdateForm(instance=profile)  # re-render with updated data
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'user_management/update_profile.html', {'form': form})
