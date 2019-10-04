"""
Provide tests for implementation of single user e-mail endpoint.
"""
import json
from http import HTTPStatus
from unittest.mock import patch

from django.test import TestCase

from services.models import EmailConfirmState
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
            is_email_confirmed=True,
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


class TestUserRequestEmailConfirmSingle(TestCase):
    """
    Implements tests for implementation of single user request email confirm endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.email = 'martin.fowler@gmail.com'
        self.password = 'martin.fowler.1337'

        User.objects.create_user(
            email=self.email,
            username='martin.fowler',
            password=self.password,
            is_email_confirmed=False,
        )

    @patch('services.email.Email.send')
    def test_request_to_confirm_user_email(self, mock_email_send):
        """
        Case: send request to confirm user email.
        Expect: a message with confirmed registration link has been sent to email.
        """
        expected_result = {
            'result': 'Message with confirmed registration link has been sent to the specified e-mail address.',
        }

        mock_email_send.return_value = None

        response = self.client.post('/users/email/confirm/', json.dumps({
            'email': self.email,
        }), content_type='application/json')

        assert EmailConfirmState.objects.get(email=self.email).identifier
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_request_to_confirm_user_email_with_incorrect_email(self):
        """
        Case: send request to confirm user email by incorrect email.
        Expect: enter a valid email address error message.
        """
        expected_result = {
            'errors': {
                'email': ['Enter a valid email address.'],
            },
        }

        response = self.client.post('/users/email/confirm/', json.dumps({
            'email': 'martin.fowler.1337',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code

    def test_request_to_confirm_user_email_with_non_existent_email(self):
        """
        Case: send request to confirm user email with non-existent email.
        Expect: user with specified e-mail address does not exist error message.
        """
        expected_result = {
            'error': 'User with specified e-mail address does not exist.',
        }

        response = self.client.post('/users/email/confirm/', json.dumps({
            'email': 'm.flower@gmail.com',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_request_to_confirm_user_email_without_email(self):
        """
        Case: send request to confirm user email without email.
        Expect: this field is required error message.
        """
        expected_result = {
            'errors': {
                'email': ['This field is required.'],
            },
        }

        response = self.client.post('/users/email/confirm/', json.dumps({}), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code


class TestUserEmailConfirmSingle(TestCase):
    """
    Implements tests for implementation of single user email confirm endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.email = 'martin.fowler@gmail.com'

        User.objects.create_user(
            email=self.email,
            username='martin.fowler',
            password='martin.fowler.1337',
            is_email_confirmed=False,
        )

    @patch('services.email.Email.send')
    def test_confirm_user_email(self, mock_email_send):
        """
        Case: confirm user email by user identifier.
        Expect: a registration is confirmed by the specified user identifier.
        """
        expected_result = {
            'result': 'Registration is confirmed by the specified identifier.',
        }

        mock_email_send.return_value = None

        self.client.post('/users/email/confirm/', json.dumps({
            'email': self.email,
        }), content_type='application/json')

        user_identifier = EmailConfirmState.objects.get(email=self.email).identifier

        response = self.client.post(
            f'/users/email/confirm/{user_identifier}/', json.dumps({}), content_type='application/json',
        )

        assert User.objects.get(email=self.email).is_email_confirmed
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_confirm_user_email_with_non_existent_identifier(self):
        """
        Case: confirm user email with non-existent identifier.
        Expect: user with specified identifier does not exist error message.
        """
        expected_result = {
            'error': 'User with specified identifier does not exist.',
        }

        non_existent_identifier = '770b420663614db4bac8a7ef0ae7a5a9'

        response = self.client.post(
            f'/users/email/confirm/{non_existent_identifier}/', json.dumps({}), content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.NOT_FOUND == response.status_code

    @patch('services.email.Email.send')
    def test_confirm_user_email_already_sent(self, mock_email_send):
        """
        Case: confirm user email has been already sent.
        Expect: user with specified identifier already confirmed error message.
        """
        expected_result = {
            'error': 'User with specified identifier already confirmed.',
        }

        mock_email_send.return_value = None

        self.client.post('/users/email/confirm/', json.dumps({
            'email': self.email,
        }), content_type='application/json')

        user_identifier = EmailConfirmState.objects.get(email=self.email).identifier

        self.client.post(
            f'/users/email/confirm/{user_identifier}/', json.dumps({}), content_type='application/json',
        )

        response = self.client.post(
            f'/users/email/confirm/{user_identifier}/', json.dumps({}), content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
