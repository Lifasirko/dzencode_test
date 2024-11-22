from celery import shared_task
from django.core.mail import send_mail
import logging

from backend.settings import EMAIL_HOST_USER

logger = logging.getLogger(__name__)


@shared_task
def send_email_notification(email, message):
    try:
        print(f"Attempting to send email to {email} with message: {message}")
        send_mail(
            subject="New Comment Notification",
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        print(f"Email successfully sent to {email}")
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
