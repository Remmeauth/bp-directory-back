"""
Provide constants for services implementation.
"""
from enum import Enum


class EmailSubject(Enum):
    """
    Email subject enum implementation.
    """

    RECOVER_PASSWORD_LINK = 'Password recovery link'
    BLOCK_PRODUCER_REJECTED = 'Block producer rejected'
    USER_CONFIRMING_REGISTRATION = 'Confirming registration'


class EmailBody(Enum):
    """
    Email body enum implementation.
    """

    REQUEST_PASSWORD_RECOVERY_MESSAGE = "Hi,<br><br>We've received a request to reset your password. " \
                                        "If you didn't make the request, just ignore this email. <br><br> " \
                                        "Otherwise, you can reset your password using this link: <br> " \
                                        "https://directory.remme.io/users/password/recovering/{}/ <br><br>" \
                                        "Thanks,<br>Remme"

    PASSWORD_RECOVERY_MESSAGE = "Hi,<br><br>Recently you have requested password recovery. " \
                                "Your new password: <strong>{}</strong>. <br><br>Thanks,<br>Remme"

    BLOCK_PRODUCER_REJECTED_MESSAGE = "Hi,<br><br>{}<br><br>Thanks,<br>Remme"

    USER_CONFIRMING_REGISTRATION_MESSAGE = "Hi,<br><br>" \
                                           "You're only one step for being able to log in on our website! <br><br>" \
                                           "Simply click on the link below to confirm your account and sign in: <br> " \
                                           "https://directory.remme.io/users/email/confirm/{}/ <br><br> " \
                                           "Thanks,<br>Remme"
