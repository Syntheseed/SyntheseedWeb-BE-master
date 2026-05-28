from rest_framework import generics, permissions
from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactAdminListView(generics.ListAPIView):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAdminUser]
