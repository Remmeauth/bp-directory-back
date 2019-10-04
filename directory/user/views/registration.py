"""
Provide implementation of single user registration endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from user.domain.errors import (
    UserWithSpecifiedEmailAddressAlreadyExistsError,
    UserWithSpecifiedUsernameAlreadyExistsError,
)
from user.domain.objects import RegisterUser
from user.forms import UserRegistrationForm
from user.models import User


class UserRegistrationSingle(APIView):
    """
    Single user registration endpoint implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()

    @permission_classes((AllowAny,))
    def post(self, request):
        """
        Create a user with e-mail address and password.
        """
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        form = UserRegistrationForm({
            'email': email,
            'username': username,
            'password': password,
        })

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        try:
            RegisterUser(user=self.user).by_credentials(email=email, username=username, password=password)
        except (
            UserWithSpecifiedEmailAddressAlreadyExistsError,
            UserWithSpecifiedUsernameAlreadyExistsError,
        ) as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'User has been created.'}, status=HTTPStatus.OK)
