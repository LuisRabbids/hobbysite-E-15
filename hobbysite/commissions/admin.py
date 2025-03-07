from django.contrib import admin
from .models import Commission, CommissionCategory

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title','description', 'people_required', 'created_on', 'last_updated')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('commission', 'entry', 'created_on', 'updated_on')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Commission, CommissionAdmin)