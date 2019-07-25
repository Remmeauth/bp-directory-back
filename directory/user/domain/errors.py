"""
Provide errors for user domain objects.
"""


class UserWithSpecifiedEmailAddressAlreadyExistsError(Exception):
    """
    User with specified e-mail address already exists error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'User with specified e-mail address already exists.'


class UserWithSpecifiedUsernameAlreadyExistsError(Exception):
    """
    User with specified username already exists error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'User with specified username already exists.'


class UserWithSpecifiedEmailAddressDoesNotExistError(Exception):
    """
    User with specified e-mail address does not exist error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'User with specified e-mail address does not exist.'


class UserWithSpecifiedUsernameDoesNotExistError(Exception):
    """
    User with specified username does not exist error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'User with specified username does not exist.'


class UserWithSpecifiedIdentifierDoesNotExistError(Exception):
    """
    User with specified identifier does not exist error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'User with specified identifier does not exist.'


class SpecifiedUserPasswordIsIncorrectError(Exception):
    """
    The specified user password is incorrect error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'The specified user password is incorrect.'


class RecoveryPasswordHasBeenAlreadySentError(Exception):
    """
    Recovery password has been already sent to e-mail address error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'Recovery password has been already sent to e-mail address.'
