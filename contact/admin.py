from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'message_preview', 'created_at']
    list_display_links = ['id', 'name']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    list_per_page = 25

    def message_preview(self, obj):
        # show a short preview of the message in list view
        if not obj.message:
            return ''
        return (obj.message[:75] + '...') if len(obj.message) > 75 else obj.message
    message_preview.short_description = 'Message'
