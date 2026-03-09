from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    read_more_url = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'category',
            'summary', 'content', 'created_at',
            'image', 'read_more_url'
        ]

    # Convert image field to absolute URL
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    # Fix CKEditor relative URLs inside HTML
    def _fix_html_media_urls(self, html, request):
        if not html:
            return html

        media_url = request.build_absolute_uri("/media/")
        return html.replace('src="/media/', f'src="{media_url}')

    def get_summary(self, obj):
        request = self.context.get('request')
        return self._fix_html_media_urls(obj.summary, request)

    def get_content(self, obj):
        request = self.context.get('request')
        return self._fix_html_media_urls(obj.content, request)

    def get_read_more_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f"/api/blogs/{obj.slug}/")
