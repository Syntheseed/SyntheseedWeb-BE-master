from rest_framework import serializers
from .models import Career, JobApplication

class CareerSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

    class Meta:
        model = Career
        fields = [
            'id',
            'title',
            'department',
            'location',
            'work_mode',
            'job_type',
            'description',
            'tags',
            'details',
            'posted_on',
        ]

    # Convert /media/... → http://127.0.0.1:8000/media/...
    def _fix_html_media_urls(self, html, request):
        if not html:
            return html
        media_url = request.build_absolute_uri("/media/")
        return html.replace('src="/media/', f'src="{media_url}')

    def get_description(self, obj):
        request = self.context.get("request")
        return self._fix_html_media_urls(obj.description, request)

    def get_details(self, obj):
        request = self.context.get("request")
        return self._fix_html_media_urls(obj.details, request)


class JobApplicationSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            'id',
            'career',
            'career_title',
            'full_name',
            'email',
            'phone',
            'resume',
            'cover_letter',
            'applied_on',
        ]
        read_only_fields = ['applied_on']
