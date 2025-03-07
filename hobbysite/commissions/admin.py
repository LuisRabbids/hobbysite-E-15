from django.contrib import admin
from .models import Commission, CommissionCategory

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'created_on', 'last_updated')

admin.site.register(CommissionCategory)
admin.site.register(Commission, CommissionAdmin)