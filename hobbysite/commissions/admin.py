from django.contrib import admin
from .models import Commission, Comment

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(admin.BaseUserAdmin):
    inlines = [ProfileInline,]

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title','description', 'people_required', 'created_on', 'updated_on')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('commission', 'entry', 'created_on', 'updated_on')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Commission, CommissionAdmin)