from rest_framework import generics, permissions, serializers as drf_serializers
from .models import Career


class CareerAdminSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['id', 'title', 'department', 'location', 'work_mode', 'job_type',
                  'description', 'tags', 'details', 'posted_on']
        read_only_fields = ['id', 'posted_on']


class CareerAdminListCreateView(generics.ListCreateAPIView):
    queryset = Career.objects.all().order_by('-posted_on')
    serializer_class = CareerAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class CareerAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Career.objects.all()
    serializer_class = CareerAdminSerializer
    permission_classes = [permissions.IsAdminUser]
