"""
Provide implementation of single user registration endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView

from user.domain.errors import UserWithSpecifiedEmailAddressAlreadyExistsError
from user.domain.objects import RegisterUser
from user.forms import UserRegistrationForm
from user.models import User


class UserRegistrationSingle(APIView):
    """
    Single user registration endpoint implementation.
    """

    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()

    def post(self, request):
        """
        Create a user with e-mail address and password.
        """
        email = request.data.get('email')
        password = request.data.get('password')

        form = UserRegistrationForm({
            'email': email,
            'password': password,
        })

        if not form.is_valid():
            return JsonResponse(form.errors, status=HTTPStatus.BAD_REQUEST)

        try:
            RegisterUser(user=self.user).by_email(email=email, password=password)
        except UserWithSpecifiedEmailAddressAlreadyExistsError as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'User has been created.'}, status=HTTPStatus.OK)
