"""
Provide implementation of single user e-mail endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.decorators import authentication_classes
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user.domain.errors import UserWithSpecifiedUsernameDoesNotExistError
from user.domain.objects import ChangeUserEmail
from user.forms import ChangeUserEmailForm
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
