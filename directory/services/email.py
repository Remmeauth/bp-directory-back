"""
Provide implementation of email.
"""
from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Email:
    """
    Email implementation.
    """

    @staticmethod
    def send(email_to, subject, message):
        """
        Send e-mail implementation.
        """
        message = Mail(
            from_email=settings.PROJECT_EMAIL_ADDRESS,
            to_emails=email_to,
            subject=subject,
            html_content=message,
        )

        SendGridAPIClient(settings.SENDGRID_API_KEY).send(message)
