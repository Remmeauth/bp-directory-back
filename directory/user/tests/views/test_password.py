"""
Provide tests for implementation of single user password endpoint.
"""
import json
from http import HTTPStatus

from django.test import TestCase

from user.models import User


class TestUserPasswordSingle(TestCase):
    """
    Implements tests for implementation of single user password endpoint.
    """

    def setUp(self):

        User.objects.create_user(email='martin.fowler@gmail.com', password='martin.fowler.1337')

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        self.user_token = response.data.get('token')

    def test_change_user_password(self):
        """
        Case: change user password.
        Expect: user password is changed.
        """
        expected_result = {
            'result': 'Password has been changed.',
        }

        response = self.client.post('/user/password/', json.dumps({
            'old_password': 'martin.fowler.1337',
            'new_password': 'martin.f.1337',
        }), HTTP_AUTHORIZATION='JWT ' + self.user_token, content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_change_user_password_without_data(self):
        """
        Case: change user password without passwords.
        Expect: old password and new password are required.
        """
        expected_result = {
            'errors': {
                'old_password': [
                    'This field is required.',
                ],
                'new_password': [
                    'This field is required.',
                ],
            },
        }

        response = self.client.post(
            '/user/password/',
            json.dumps({}),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
