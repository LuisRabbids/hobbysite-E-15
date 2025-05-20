from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # Keep if you use this for Profile
from .models import Commission, Job, JobApplication # Removed Comment, Added Job, JobApplication
# from user_management.models import Profile # Keep if you define ProfileInline here

# If ProfileInline and UserAdmin are managed in user_management app's admin.py, you might not need them here.
# If they are general to your project and you want to keep User admin customized here, it's fine.
# For now, I'll comment them out assuming they might be in user_management's admin.py or not strictly needed for this app's admin.

# class ProfileInline(admin.StackedInline):
#    model = Profile
#    can_delete = False

# class UserAdmin(BaseUserAdmin):
#    inlines = [ProfileInline,]

class JobInline(admin.TabularInline): # Or admin.StackedInline
    model = Job
    extra = 1 # Number of empty forms to display
    fields = ('role', 'manpower_required', 'status')
    # readonly_fields = ('get_accepted_applicants_count',) # Example if you add such a method to Job model

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_username', 'status', 'created_on', 'updated_on', 'get_total_manpower', 'get_open_manpower_admin')
    list_filter = ('status', 'created_on', 'author')
    search_fields = ('title', 'description', 'author__user__username')
    readonly_fields = ('created_on', 'updated_on')
    inlines = [JobInline] # Add jobs directly in the commission admin page
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'description', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',) # Makes this section collapsible
        }),
    )

    def author_username(self, obj):
        if obj.author and obj.author.user:
            return obj.author.user.username
        return '-'
    author_username.short_description = 'Author'

    def get_total_manpower(self, obj):
        return obj.get_total_manpower_required()
    get_total_manpower.short_description = 'Total Manpower Req.'

    def get_open_manpower_admin(self, obj):
        return obj.get_open_manpower()
    get_open_manpower_admin.short_description = 'Open Manpower'


class JobAdmin(admin.ModelAdmin):
    list_display = ('role', 'commission_title', 'manpower_required', 'status', 'get_accepted_applicants_count_admin')
    list_filter = ('status', 'commission__title')
    search_fields = ('role', 'commission__title')
    readonly_fields = ('get_accepted_applicants_count_admin',)

    def commission_title(self, obj):
        return obj.commission.title
    commission_title.short_description = 'Commission'
    commission_title.admin_order_field = 'commission__title'

    def get_accepted_applicants_count_admin(self, obj):
        return obj.get_accepted_applicants_count()
    get_accepted_applicants_count_admin.short_description = 'Accepted Applicants'

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_username', 'job_role_and_commission', 'status', 'applied_on')
    list_filter = ('status', 'job__commission__title', 'job__role', 'applicant')
    search_fields = ('applicant__user__username', 'job__role', 'job__commission__title')
    readonly_fields = ('applied_on',)
    # Allow changing status in admin
    list_editable = ('status',) # Be cautious with list_editable, ensure proper permissions

    def applicant_username(self, obj):
        if obj.applicant and obj.applicant.user:
            return obj.applicant.user.username
        return '-'
    applicant_username.short_description = 'Applicant'
    applicant_username.admin_order_field = 'applicant__user__username'

    def job_role_and_commission(self, obj):
        return f"{obj.job.role} (for {obj.job.commission.title})"
    job_role_and_commission.short_description = 'Job'
    job_role_and_commission.admin_order_field = 'job__role' # or 'job__commission__title'

# Register your models here
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)

# Removed:
# admin.site.register(Comment, CommentAdmin)