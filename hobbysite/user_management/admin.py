from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'get_email')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
