"""
Provide tests for implementation of single user endpoint.
"""
from http import HTTPStatus

from django.test import TestCase

from user.models import User


class TestUserSingle(TestCase):
    """
    Implements tests for implementation of single user endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.user = User.objects.create_user(
            id=99,
            email='martin.fowler@gmail.com',
            username='martin.fowler',
            password='martin.fowler.1337',
        )

    def test_get_user_by_username(self):
        """
        Case: get user.
        Expect: user information is returned.
        """
        expected_result = {
            'result': {
                'email': 'martin.fowler@gmail.com',
                'id': 99,
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
                'last_login': None,
                'username': 'martin.fowler',
            },
        }

        response = self.client.get('/user/martin.fowler/', content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_get_user_by_non_existing_username(self):
        """
        Case: get user by non-existing username.
        Expect: user with specified username does not exist error message.
        """
        expected_result = {
            'error': 'User with specified username does not exist.',
        }

        response = self.client.get('/user/not.martin.fowler/', content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
