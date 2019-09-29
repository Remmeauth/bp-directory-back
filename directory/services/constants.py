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


class EmailBody(Enum):
    """
    Email body enum implementation.
    """

    REQUEST_PASSWORD_RECOVERY_MESSAGE = "Hi,<br><br>We've received a request to reset your password. " \
                                        "If you didn't make the request, just ignore this email. <br><br> " \
                                        "Otherwise, you can reset your password using this link: <br> " \
                                        "https://directory.remme.io/user/password/recovering/{}/ <br><br>" \
                                        "Thanks,<br>Remme"

    PASSWORD_RECOVERY_MESSAGE = "Hi,<br><br>Recently you have requested password recovery. " \
                                "Your new password: <strong>{}</strong>. <br><br>Thanks,<br>Remme"

    BLOCK_PRODUCER_REJECTED_MESSAGE = "Hi,<br><br>Recently you have requested password recovery. " \
                                      "Your new password: <strong>{}</strong>. <br><br>Thanks,<br>Remme"
