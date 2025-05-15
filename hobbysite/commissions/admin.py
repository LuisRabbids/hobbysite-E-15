from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Commission, Comment
from user_management.models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline,]

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title','description', 'people_required', 'created_on', 'updated_on')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('commission', 'entry', 'created_on', 'updated_on')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Commission, CommissionAdmin)