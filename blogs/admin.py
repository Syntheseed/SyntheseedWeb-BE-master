from django.contrib import admin
from django.utils.html import format_html
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'summary_preview', 'image_tag')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'category', 'summary', 'content')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 25

    def summary_preview(self, obj):
        if not obj.summary:
            return ''
        return (obj.summary[:80] + '...') if len(obj.summary) > 80 else obj.summary
    summary_preview.short_description = 'Summary'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;"/>', obj.image.url)
        return ''
    image_tag.short_description = 'Image'

