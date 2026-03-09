from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from .email_service import send_contact_notification_async
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
@authentication_classes([])          
@permission_classes([AllowAny])       
def submit_contact_form(request):
    print("🔥 submit_contact_form reached!")  
    logger.debug("Received POST request to /api/contact/submit/")
    logger.debug(f"User: {request.user}, Auth: {request.auth}")

    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # send notification asynchronously to configured recipient(s)
        try:
            recipients = []
            raw = getattr(settings, 'NOTIFY_CONTACT_RECIPIENTS', None)
            if raw:
                if isinstance(raw, list):
                    recipients = raw
                else:
                    recipients = [raw]
            else:
                # fallback to configured default sender/recipient
                default_recipient = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'AZURE_SENDER_UPN', None)
                if default_recipient:
                    recipients = [default_recipient]
                else:
                    recipients = []

            # pass the saved instance to the async sender
            instance = serializer.instance
            send_contact_notification_async(instance, recipients)
        except Exception:
            logger.exception('Failed to schedule contact notification email')
        logger.info("✅ Contact message saved successfully")
        return Response(
            {"message": "Message received successfully!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        logger.warning(f"❌ Invalid data: {serializer.errors}")
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
