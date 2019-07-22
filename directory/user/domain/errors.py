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


class SpecifiedUserPasswordWasIncorrectError(Exception):
    """
    The specified user password was incorrect error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'The specified user password was incorrect.'
