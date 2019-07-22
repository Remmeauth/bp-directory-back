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


class UserWithSpecifiedEmailAddressDoesNotExistError(Exception):
    """
    User with specified e-mail address does not exist error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'User with specified e-mail address does not exist.'


class SpecifiedUserPasswordIsIncorrectError(Exception):
    """
    The specified user password is incorrect error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'The specified user password is incorrect.'
