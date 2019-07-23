"""
Provide implementation of email.
"""
from django.conf import settings
from django.core.mail import send_mail


class Email:
    """
    Email implementation.
    """

    @staticmethod
    def send(email_to, subject, message):
        """
        Send e-mail implementation.
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email_to],
            fail_silently=True,
        )
