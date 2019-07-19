"""
Provide implementation of user registration.
"""
from user.domain.errors import UserWithSpecifiedEmailAddressAlreadyExistsError


class RegisterUser:
    """
    User registration implementation.
    """

    def __init__(self, user):
        """
        Constructor.
        """
        self.user = user

    def by_email(self, email, password):
        """
        Create a user with specified e-mail address and password.
        """
        if self.user.does_exist(email=email):
            raise UserWithSpecifiedEmailAddressAlreadyExistsError

        self.user.create_with_email(email=email, password=password)
