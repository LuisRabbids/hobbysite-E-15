from django.contrib import admin
from .models import Commission, CommissionCategory

class CommissionAdmin(admin.ModelAdmin):
    model = Commission

class CommissionCategoryAdmin(admin.ModelAdmin):
    model = CommissionCategory

admin.site.register(CommissionCategory)
admin.site.register(Commission)