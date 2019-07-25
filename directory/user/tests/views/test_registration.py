"""
Provide test for implementation of single user registration endpoint.
"""
import json
from http import HTTPStatus

from django.test import TestCase

from user.models import User


class TestUserRegistrationSingle(TestCase):
    """
    Implements test for implementation of single user registration endpoint.
    """

    def test_register_user(self):
        """
        Case: register user with e-mail and password.
        Expect: user with specified e-mail and password is created.
        """
        expected_result = {
            'result': 'User has been created.',
        }

        response = self.client.post('/user/registration/', json.dumps({
            'email': 'martin.fowler@gmail.com',
            'username': 'martin.fowler',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_register_already_existing_email(self):
        """
        Case: register already existing user with e-mail address.
        Expect: user with specified e-mail address already exists error message.
        """
        User.objects.create_user(
            email='martin.fowler@gmail.com',
            username='martin.fowler',
            password='martin.fowler.1337',
        )

        expected_result = {
            'error': 'User with specified e-mail address already exists.',
        }

        response = self.client.post('/user/registration/', json.dumps({
            'email': 'martin.fowler@gmail.com',
            'username': 'martin.fowler',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code

    def test_register_already_existing_username(self):
        """
        Case: register already existing user with username.
        Expect: user with specified username already exists error message.
        """
        User.objects.create_user(
            email='martin.fowler@gmail.com',
            username='martin.fowler',
            password='martin.fowler.1337',
        )

        expected_result = {
            'error': 'User with specified username already exists.',
        }

        response = self.client.post('/user/registration/', json.dumps({
            'email': 'not.martin.fowler@gmail.com',
            'username': 'martin.fowler',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code

    def test_register_user_with_no_data(self):
        """
        Case: register user without e-mail address and password.
        Expect: e-mail address and password are required.
        """
        expected_result = {
            'errors': {
                'email': [
                    'This field is required.',
                ],
                'username': [
                    'This field is required.',
                ],
                'password': [
                    'This field is required.',
                ],
            },
        }

        response = self.client.post('/user/registration/', json.dumps({}), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
