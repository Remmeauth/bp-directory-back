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
