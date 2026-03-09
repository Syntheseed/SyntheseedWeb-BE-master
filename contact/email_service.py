from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from django.conf import settings

try:
    # local import, will be present if we added graph_email.py
    from .graph_email import send_mail_via_graph_async
except Exception:
    send_mail_via_graph_async = None

logger = logging.getLogger(__name__)

# a small thread pool for background email sending
_executor = ThreadPoolExecutor(max_workers=2)


def _send_email_sync(subject, html_content, text_content, from_email, to_emails):
    try:
        msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=to_emails)
        if html_content:
            msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info('SMTP email sent. From: %s To: %s', from_email, to_emails)
        print(f"SMTP email sent. From: {from_email} To: {to_emails}")
    except Exception as exc:
        logger.exception("Failed to send email: %s", exc)


def send_contact_notification_async(contact_obj, to_email_list):
    
    try:
        context = {
            'name': getattr(contact_obj, 'name', ''),
            'email': getattr(contact_obj, 'email', ''),
            'phone': getattr(contact_obj, 'phone', ''),
            'subject': getattr(contact_obj, 'subject', ''),
            'message': getattr(contact_obj, 'message', ''),
            'created_at': getattr(contact_obj, 'created_at', None),
        }
        html_content = render_to_string('contact/contact_submission.html', context)
        text_content = strip_tags(html_content)
        subject = f"New contact form submission: {context['subject'] or 'No subject'}"
        # determine a sensible from_email: prefer DEFAULT_FROM_EMAIL, then AZURE_SENDER_UPN, then the first recipient
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'AZURE_SENDER_UPN', None)
        if not from_email:
            # fallback to first recipient if nothing else is configured
            from_email = to_email_list[0] if to_email_list else None

        # Determine and log sender/recipients
        logger.info('Preparing contact notification. From: %s To: %s', from_email, to_email_list)

        # Optionally include sender in recipients for testing
        try:
            send_copy = bool(getattr(settings, 'SEND_COPY_TO_SENDER', False))
        except Exception:
            send_copy = False
        if send_copy:
            sender_upn = getattr(settings, 'AZURE_SENDER_UPN', None) or getattr(settings, 'DEFAULT_FROM_EMAIL', None)
            if sender_upn and sender_upn not in to_email_list:
                logger.info('Including sender in recipients for testing: %s', sender_upn)
                to_email_list = list(to_email_list) + [sender_upn]

        # Prefer Graph-based sending if Azure credentials are present
        azure_client_id = getattr(settings, 'AZURE_CLIENT_ID', None)
        azure_client_secret = getattr(settings, 'AZURE_CLIENT_SECRET', None)
        azure_tenant = getattr(settings, 'AZURE_TENANT_ID', None)
        azure_sender = getattr(settings, 'AZURE_SENDER_UPN', None)

        if all([azure_client_id, azure_client_secret, azure_tenant, azure_sender]) and send_mail_via_graph_async:
            try:
                send_mail_via_graph_async(contact_obj, to_email_list)
                logger.info('Scheduled Graph email send')
                print('Scheduled Graph email send')
                return
            except Exception:
                logger.exception('Graph send failed, falling back to SMTP')

        # submit to thread pool (SMTP fallback)
        _executor.submit(_send_email_sync, subject, html_content, text_content, from_email, to_email_list)
    except Exception:
        logger.exception('Error preparing contact notification email')
