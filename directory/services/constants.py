"""
Provide constants for services implementation.
"""
from enum import Enum


class EmailSubject(Enum):
    """
    Email subject enum implementation.
    """

    RECOVER_PASSWORD_LINK = 'Password recovery link'


class EmailBody(Enum):
    """
    Email body enum implementation.
    """

    REQUEST_PASSWORD_RECOVERY_MESSAGE = "Hi,\n\nWe've received a request to reset your password. " \
                                        "If you didn't make the request, just ignore this email. " \
                                        "Otherwise, you can reset your password using this link: \n" \
                                        "https://directory.com/user/password/recovering/{}/\n\nThanks,\nRemme"

    PASSWORD_RECOVERY_MESSAGE = "Hi,\n\nRecently you have requested password recovery. Your new password is {}" \
                                ".\n\nThanks,\nRemme"
