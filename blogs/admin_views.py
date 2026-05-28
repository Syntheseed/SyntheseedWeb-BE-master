from rest_framework import generics, permissions, parsers, serializers as drf_serializers
from .models import Blog


class BlogAdminSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'category', 'summary', 'content', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {'slug': {'required': False, 'allow_blank': True}}


class BlogAdminListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]


class BlogAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
