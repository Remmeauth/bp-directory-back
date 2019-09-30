"""
Provide implementation of single user e-mail endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from services.constants import (
    EmailBody,
    EmailSubject,
)
from services.email import Email
from services.models import EmailConfirmState
from user.domain.errors import (
    UserWithSpecifiedEmailAddressDoesNotExistError,
    UserWithSpecifiedIdentifierAlreadyConfirmedError,
    UserWithSpecifiedIdentifierDoesNotExistError,
    UserWithSpecifiedUsernameDoesNotExistError,
)
from user.domain.objects import (
    ChangeUserEmail,
    UserEmailConfirm,
    UserRequestEmailConfirm,
)
from user.forms import (
    ChangeUserEmailForm,
    UserEmailConfirmForm,
)
from user.models import User


class UserEmailSingle(APIView):
    """
    Single user email endpoint implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()

    @authentication_classes((JSONWebTokenAuthentication, ))
    def post(self, request, username):
        """
        Change user e-mail.
        """
        new_email = request.data.get('new_email')

        form = ChangeUserEmailForm({
            'new_email': new_email,
        })

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        try:
            ChangeUserEmail(user=self.user).do(username=username, new_email=new_email)
        except UserWithSpecifiedUsernameDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.NOT_FOUND)

        return JsonResponse({'result': 'E-mail has been changed.'}, status=HTTPStatus.OK)


class UserRequestEmailConfirmSingle(APIView):
    """
    Single user request email confirm endpoint implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.email_service = Email()
        self.email_confirm_state = EmailConfirmState()

    @permission_classes((AllowAny,))
    def post(self, request):
        """
        Request email confirm at the specified email address.
        """
        email = request.data.get('email')

        form = UserEmailConfirmForm({
            'email': email,
        })

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        try:
            confirm_identifier = UserRequestEmailConfirm(
                user=self.user, email_confirm_state=self.email_confirm_state,
            ).do(email=email)

        except UserWithSpecifiedEmailAddressDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.NOT_FOUND)

        message = EmailBody.USER_CONFIRMING_REGISTRATION_MESSAGE.value.format(confirm_identifier)

        self.email_service.send(
            email_to=email, subject=EmailSubject.USER_CONFIRMING_REGISTRATION.value, message=message,
        )

        return JsonResponse(
            {'result': 'Message with confirmed registration link has been sent to the specified e-mail address.'},
            status=HTTPStatus.OK,
        )


class UserEmailConfirmSingle(APIView):
    """
    Single user email confirm endpoint implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()
        self.email_service = Email()
        self.email_confirm_state = EmailConfirmState()

    @permission_classes((AllowAny,))
    def post(self, request, user_identifier):
        """
        Confirm registration at the specified user identifier.
        """
        try:
            UserEmailConfirm(
                user=self.user, email_confirm_state=self.email_confirm_state,
            ).do(user_identifier=user_identifier)

        except UserWithSpecifiedIdentifierDoesNotExistError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.NOT_FOUND)
        except UserWithSpecifiedIdentifierAlreadyConfirmedError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse(
            {'result': 'Registration is confirmed by the specified identifier.'},
            status=HTTPStatus.OK,
        )
