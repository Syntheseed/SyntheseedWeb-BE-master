import logging
import json
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def _build_message_payload(subject, html_content, to_emails, from_email):
    # Graph message JSON structure
    body = {
        "contentType": "html",
        "content": html_content,
    }
    to_recipients = [{"emailAddress": {"address": addr}} for addr in to_emails]

    message = {
        "subject": subject,
        "body": body,
        "toRecipients": to_recipients,
    }
    return {"message": message, "saveToSentItems": "true"}


def send_mail_via_graph(contact_obj, recipients):
 
    try:
        import msal
        import requests
    except Exception as exc:
        logger.exception("msal or requests not installed: %s", exc)
        raise

    client_id = getattr(settings, 'AZURE_CLIENT_ID', None)
    client_secret = getattr(settings, 'AZURE_CLIENT_SECRET', None)
    tenant_id = getattr(settings, 'AZURE_TENANT_ID', None)
    sender_upn = getattr(settings, 'AZURE_SENDER_UPN', None)

    if not all([client_id, client_secret, tenant_id, sender_upn]):
        raise RuntimeError('Azure Graph credentials (AZURE_CLIENT_ID/AZURE_CLIENT_SECRET/AZURE_TENANT_ID/AZURE_SENDER_UPN) are required for Graph email sending')

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scope = ["https://graph.microsoft.com/.default"]

    app = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
    token_resp = app.acquire_token_for_client(scopes=scope)

    if 'access_token' not in token_resp:
        logger.error('Failed to acquire access token: %s', token_resp)
        raise RuntimeError('Could not acquire access token for Microsoft Graph')

    access_token = token_resp['access_token']

    # render template for body
    context = {
        'name': getattr(contact_obj, 'name', ''),
        'email': getattr(contact_obj, 'email', ''),
        'phone': getattr(contact_obj, 'phone', ''),
        'subject': getattr(contact_obj, 'subject', ''),
        'message': getattr(contact_obj, 'message', ''),
        'created_at': getattr(contact_obj, 'created_at', None),
    }
    html_content = render_to_string('contact/contact_submission.html', context)
    subject = f"New contact form submission: {context['subject'] or 'No subject'}"

    payload = _build_message_payload(subject, html_content, recipients, sender_upn)

    url = f"https://graph.microsoft.com/v1.0/users/{sender_upn}/sendMail"
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }

    resp = requests.post(url, headers=headers, data=json.dumps(payload))
    if resp.status_code not in (200, 202):
        logger.error('Graph sendMail failed (status %s). Sender: %s Recipients: %s Response: %s', resp.status_code, sender_upn, recipients, resp.text)
        resp.raise_for_status()

    logger.info('Graph email sent. Sender: %s Recipients: %s', sender_upn, recipients)


def send_mail_via_graph_async(contact_obj, recipients):
    # import ThreadPoolExecutor lazily to keep module light
    from concurrent.futures import ThreadPoolExecutor

    executor = ThreadPoolExecutor(max_workers=1)
    logger.info('Scheduling Graph send. Sender: %s Recipients: %s', getattr(settings, 'AZURE_SENDER_UPN', None), recipients)
    executor.submit(send_mail_via_graph, contact_obj, recipients)
