"""
Provide tests for implementation of single user e-mail endpoint.
"""
import json
from http import HTTPStatus

from django.test import TestCase

from user.models import User


class TestUserPasswordSingle(TestCase):
    """
    Implements tests for implementation of single user e-mail endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.user = User.objects.create_user(
            email='martin.fowler@gmail.com',
            username='martin.fowler',
            password='martin.fowler.1337',
        )

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'username_or_email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        self.user_token = response.data.get('token')

    def test_change_user_email(self):
        """
        Case: change user e-mail by specified username.
        Expect: user e-mail is changed.
        """
        expected_result = {
            'result': 'E-mail has been changed.',
        }

        response = self.client.post('/users/martin.fowler/email/', json.dumps({
            'new_email': 'martin.fowler.1337@gmail.com',
        }), HTTP_AUTHORIZATION='JWT ' + self.user_token, content_type='application/json')

        assert User.objects.get(username='martin.fowler').email == 'martin.fowler.1337@gmail.com'
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_change_user_email_by_non_existing_username(self):
        """
        Case: change user e-mail by non-existing username.
        Expect: user with specified username does not exist error message.
        """
        expected_result = {
            'error': 'User with specified username does not exist.',
        }

        response = self.client.post('/users/not.martin.fowler/email/', json.dumps({
            'new_email': 'martin.fowler.1337@gmail.com',
        }), HTTP_AUTHORIZATION='JWT ' + self.user_token, content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_change_user_email_without_data(self):
        """
        Case: change user e-mail without passwords.
        Expect: new_email field is required error message.
        """
        expected_result = {
            'errors': {
                'new_email': ['This field is required.'],
            },
        }

        response = self.client.post(
            '/users/martin.fowler/email/', HTTP_AUTHORIZATION='JWT ' + self.user_token, content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
