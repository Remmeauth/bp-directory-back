"""
Provide implementation of user registration.
"""
from user.domain.errors import (
    SpecifiedUserPasswordWasIncorrectError,
    UserWithSpecifiedEmailAddressAlreadyExistsError,
    UserWithSpecifiedEmailAddressDoesNotExistError,
)


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


class ChangeUserPassword:
    """
    User password implementation.
    """

    def __init__(self, user):
        """
        Constructor.
        """
        self.user = user

    def do(self, email, old_password, new_password):
        """
        Change user password.
        """
        if not self.user.does_exist(email=email):
            raise UserWithSpecifiedEmailAddressDoesNotExistError

        is_password_matched = self.user.verify_password(email=email, password=old_password)

        if is_password_matched is False:
            raise SpecifiedUserPasswordWasIncorrectError

        self.user.set_new_password(email=email, password=new_password)
