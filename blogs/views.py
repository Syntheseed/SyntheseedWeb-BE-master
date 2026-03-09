from rest_framework import generics
from .models import Blog
from .serializers import BlogSerializer

class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer

    # Pass request -> serializer (REQUIRED for absolute URLs)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class BlogDetailAPIView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'

    # Pass request -> serializer (REQUIRED for absolute URLs)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
