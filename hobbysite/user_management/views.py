from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Profile
from .forms import ProfileUpdateForm


@login_required
def update_profile(request, display_name):
    profile = get_object_or_404(Profile, display_name=display_name)

    if profile.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this profile.")

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # reload with saved data
            form = ProfileUpdateForm(instance=profile)
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'user_management/update_profile.html', {'form': form})
