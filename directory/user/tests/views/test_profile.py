"""
Provide tests for implementation of single user profile endpoint.
"""
import json
from http import HTTPStatus

from django.test import TestCase

from user.models import (
    Profile,
    User,
)


class TestUserProfileSingle(TestCase):
    """
    Implements tests for implementation of single user profile endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.user = User.objects.create_user(email='martin.fowler@gmail.com', password='martin.fowler.1337')

        Profile.objects.create(user=self.user, first_name='John')

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        self.user_token = response.data.get('token')

    def test_update_user_profile(self):
        """
        Case: update user profile.
        Expect: user profile is updated.
        """
        expected_result = {
            'result': 'User profile has been updated.',
        }

        response = self.client.post('/user/profile/', json.dumps({
            'first_name': 'Martin',
            'last_name': 'Fowler',
            'location': 'Berlin, Germany',
            'additional_information': 'Software Engineer at Travis-CI.',
            'website_url': 'https://martinfowler.com',
            'linkedin_url': 'https://www.linkedin.com/in/martinfowler',
        }), HTTP_AUTHORIZATION='JWT ' + self.user_token, content_type='application/json')

        assert Profile.objects.get(user=self.user).first_name == 'Martin'
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code
