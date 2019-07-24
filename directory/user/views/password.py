"""
Provide implementation of single user password endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from services.constants import (
    EmailBody,
    EmailSubject,
)
from services.email import Email
from services.models import PasswordRecoveryState
from user.domain.errors import (
    RecoveryPasswordHasBeenAlreadySentError,
    SpecifiedUserPasswordIsIncorrectError,
    UserWithSpecifiedEmailAddressDoesNotExistError,
    UserWithSpecifiedIdentifierDoesNotExistError,
)
from user.domain.objects import (
    ChangeUserPassword,
    RecoverUserPassword,
    RequestUserPasswordRecovery,
)
from user.forms import (
    ChangeUserPasswordForm,
    RestoreUserPasswordForm,
)
from user.models import User


class UserPasswordSingle(APIView):
    """
    Single user password endpoint implementation.
    """

    authentication_classes = (JSONWebTokenAuthentication,)

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()

    def post(self, request):
        """
        Change user password.
        """
        email = request.user.email

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        form = ChangeUserPasswordForm({
            'old_password': old_password,
            'new_password': new_password,
        })

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        try:
            ChangeUserPassword(user=self.user).do(email=email, old_password=old_password, new_password=new_password)
        except (
            SpecifiedUserPasswordIsIncorrectError,
            UserWithSpecifiedEmailAddressDoesNotExistError,
        ) as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'Password has been changed.'}, status=HTTPStatus.OK)


class UserRequestPasswordRecoverySingle(APIView):
    """
    Single request to recover user password endpoint implementation.
    """

    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.email_service = Email()
        self.password_recovery_state = PasswordRecoveryState()

    def post(self, request):
        """
        Request to recover user password by email.

        Send message to the specified e-mail with password as message.
        """
        email = request.data.get('email')

        form = RestoreUserPasswordForm({
            'email': email,
        })

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        try:
            recovery_identifier = RequestUserPasswordRecovery(
                user=self.user, password_recovery_state=self.password_recovery_state,
            ).do(email=email)

        except UserWithSpecifiedEmailAddressDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        message = EmailBody.REQUEST_PASSWORD_RECOVERY_MESSAGE.value.format(recovery_identifier)

        self.email_service.send(
            email_to=email, subject=EmailSubject.RECOVER_PASSWORD_LINK.value, message=message,
        )

        return JsonResponse(
            {'result': 'Recovery link has been sent to the specified e-mail address.'}, status=HTTPStatus.OK,
        )


class UserPasswordRecoverSingle(APIView):
    """
    Single user password recover endpoint implementation.
    """

    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.email_service = Email()
        self.password_recovery_state = PasswordRecoveryState()

    def post(self, request, user_identifier):
        """
        Recover user password by user identifier.

        Send message to e-mail with a new password as message.
        """
        try:
            email, new_password = RecoverUserPassword(
                user=self.user, password_recovery_state=self.password_recovery_state,
            ).do(user_identifier=user_identifier)

        except (
            RecoveryPasswordHasBeenAlreadySentError,
            UserWithSpecifiedIdentifierDoesNotExistError,
        )as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        message = EmailBody.PASSWORD_RECOVERY_MESSAGE.value.format(new_password)

        self.email_service.send(
            email_to=email, subject=EmailSubject.RECOVER_PASSWORD_LINK.value, message=message,
        )

        return JsonResponse(
            {'result': 'New password has been sent to e-mail address.'}, status=HTTPStatus.OK,
        )
