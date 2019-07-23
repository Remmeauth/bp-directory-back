"""
Provide errors for services objects.
"""


class UserWithSpecifiedIdentifierDoesNotExistError(Exception):
    """
    User with specified identifier does not exist error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'User with specified identifier does not exist.'


class RecoveryPasswordHasBeenAlreadySentError(Exception):
    """
    Recovery password has been already sent to e-mail address error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'Recovery password has been already sent to e-mail address.'
