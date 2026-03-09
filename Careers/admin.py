from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Career

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'department', 'location',
        'work_mode', 'job_type', 'posted_on'
    )
    list_filter = (
        'department', 'location', 'work_mode',
        'job_type', 'posted_on'
    )
    search_fields = (
        'title', 'department', 'location', 'tags', 'description'
    )
    readonly_fields = ('posted_on',)
    ordering = ('-posted_on',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'department', 'location', 'work_mode', 'job_type')
        }),
        ('Content', {
            'fields': ('description', 'details', 'tags')
        }),
        ('Metadata', {
            'fields': ('posted_on',)
        }),
    )
    
from .models import JobApplication


# class JobApplicationInline(admin.TabularInline):
#     model = JobApplication
#     fields = ('full_name', 'email', 'phone', 'applied_on')
#     readonly_fields = ('full_name', 'email', 'phone', 'applied_on')
#     extra = 0
#     show_change_link = True


# @admin.register(JobApplication)
# class JobApplicationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'career', 'full_name', 'email', 'applied_on')
#     list_filter = ('applied_on', 'career')
#     search_fields = ('full_name', 'email', 'career__title')
#     readonly_fields = ('applied_on',)
#     ordering = ('-applied_on',)
#     list_select_related = ('career',)

# # attach inline below CareerAdmin definition to avoid forward ref issues
# CareerAdmin.inlines = [JobApplicationInline]