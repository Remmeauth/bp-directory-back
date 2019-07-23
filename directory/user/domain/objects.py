"""
Provide implementation of user registration.
"""
import uuid

from services.errors import (
    RecoveryPasswordHasBeenAlreadySentError,
    UserWithSpecifiedIdentifierDoesNotExistError,
)
from user.domain.errors import (
    SpecifiedUserPasswordIsIncorrectError,
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
    Change user password implementation.
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

        if not is_password_matched:
            raise SpecifiedUserPasswordIsIncorrectError

        self.user.set_new_password(email=email, password=new_password)


class RequestUserPasswordRecovery:
    """
    Request to recovery user password implementation.
    """

    def __init__(self, user, password_recovery_state):
        """
        Constructor.
        """
        self.user = user
        self.password_recovery_state = password_recovery_state

    def do(self, email):
        """
        Request to recover user password by email.
        """
        if not self.user.does_exist(email=email):
            raise UserWithSpecifiedEmailAddressDoesNotExistError

        identifier = uuid.uuid4().hex

        self.password_recovery_state.create(email=email, identifier=identifier)

        return identifier


class RecoveryUserPassword:
    """
    Recovery user password implementation.
    """

    def __init__(self, user, password_recovery_state):
        """
        Constructor.
        """
        self.user = user
        self.password_recovery_state = password_recovery_state

    def do(self, user_identifier):
        """
        Recovery user password by user identifier.
        """
        if not self.password_recovery_state.does_exist(user_identifier=user_identifier):
            raise UserWithSpecifiedIdentifierDoesNotExistError

        if not self.password_recovery_state.is_active_(user_identifier=user_identifier):
            raise RecoveryPasswordHasBeenAlreadySentError

        self.password_recovery_state.deactivate(user_identifier=user_identifier)

        email = self.password_recovery_state.get_email(user_identifier=user_identifier)

        new_password = uuid.uuid4().hex[:12]

        self.user.set_new_password(email=email, password=new_password)
        return email, new_password
