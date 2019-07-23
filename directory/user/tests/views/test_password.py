"""
Provide tests for implementation of single user password endpoint.
"""
import json
from http import HTTPStatus

from django.test import TestCase

from services.models import PasswordRecoveryState
from user.models import User


class TestUserPasswordSingle(TestCase):
    """
    Implements tests for implementation of single user password endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
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

    def test_change_user_password_with_incorrect_password(self):
        """
        Case: change user password with incorrect password.
        Expect: specified user password is incorrect error message.
        """
        expected_result = {
            'error': 'The specified user password is incorrect.',
        }

        response = self.client.post('/user/password/', json.dumps({
            'old_password': 'martin.fowler.1111',
            'new_password': 'martin.f.1337',
        }), HTTP_AUTHORIZATION='JWT ' + self.user_token, content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code

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


class TestUserRequestPasswordRecoverySingle(TestCase):
    """
    Implements tests for implementation of single request to recover user password endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.email = 'martin.fowler@gmail.com'
        self.password = 'martin.fowler.1337'

        User.objects.create_user(email=self.email, password=self.password)

    def test_request_recover_user_password(self):
        """
        Case: sent request to recover user password by email.
        Expect: a password recovery email has been sent.
        """
        expected_result = {
            'result': 'Forgotten password has been sent to the specified e-mail address.',
        }

        response = self.client.post('/user/password/recovery/', json.dumps({
            'email': self.email,
        }), content_type='application/json')

        assert PasswordRecoveryState.objects.get(email=self.email).identifier
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_request_recover_user_password_with_incorrect_email(self):
        """
        Case: sent request to recover user password by incorrect email.
        Expect: enter a valid email address error message.
        """
        expected_result = {
            'errors': {
                'email': ['Enter a valid email address.'],
            },
        }

        response = self.client.post('/user/password/recovery/', json.dumps({
            'email': 'martin.fowler.1337',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code

    def test_request_recover_user_password_with_non_existent_email(self):
        """
        Case: sent request to recover user password with non-existent email.
        Expect: user with specified e-mail address does not exist error message.
        """
        expected_result = {
            'error': 'User with specified e-mail address does not exist.',
        }

        response = self.client.post('/user/password/recovery/', json.dumps({
            'email': 'martin.flower@gmail.com',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code

    def test_request_recover_user_password_without_email(self):
        """
        Case: sent request to recover user password without email.
        Expect: this field is required error message.
        """
        expected_result = {
            'errors': {
                'email': ['This field is required.'],
            },
        }

        response = self.client.post('/user/password/recovery/', json.dumps({}), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code


class TestUserPasswordRecoverySingle(TestCase):
    """
    Implements tests for implementation of single user password recovery endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.email = 'martin.fowler@gmail.com'
        self.password = 'martin.fowler.1337'

        self.user = User.objects.create_user(email=self.email, password='martin.fowler.1337')

        self.client.post('/user/password/recovery/', json.dumps({
            'email': self.email,
        }), content_type='application/json')

    def test_recovery_user_password(self):
        """
        Case: recovery user password by user identifier.
        Expect: a password recovery email with new password has been sent.
        """
        expected_result = {
            'result': 'New password has been sent to e-mail address.',
        }

        self.user_identifier = PasswordRecoveryState.objects.get(email=self.email).identifier

        response = self.client.post(
            f'/user/password/recovery/{self.user_identifier}', json.dumps({}), content_type='application/json',
        )

        assert User.objects.get(email=self.email).password != self.password
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_recovery_user_password_with_non_existent_identifier(self):
        """
        Case: recovery user password with non-existent identifier.
        Expect: user with specified identifier does not exist error message.
        """
        expected_result = {
            'error': 'User with specified identifier does not exist.',
        }

        non_existent_identifier = '770b420663614db4bac8a7ef0ae7a5a9'

        response = self.client.post(
            f'/user/password/recovery/{non_existent_identifier}', json.dumps({}), content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
