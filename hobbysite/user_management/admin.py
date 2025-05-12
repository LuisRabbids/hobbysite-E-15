from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'email')  # Display fields in the list view
    fields = ('user', 'display_name', 'email')  # Fields to show in the form view


admin.site.register(Profile, ProfileAdmin)