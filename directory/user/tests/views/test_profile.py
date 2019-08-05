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
        self.username = 'martin.fowler'
        self.user = User.objects.create_user(
            email='martin.fowler@gmail.com', username=self.username, password='martin.fowler.1337',
        )

        Profile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Smith',
            location='Tokyo, Japan',
            additional_information='Senior Software Engineer at Yamaha.',
            website_url='https://johnsmith.com',
        )

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'username_or_email': 'martin.fowler@gmail.com',
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

        response = self.client.post(f'/user/{self.username}/profile/', json.dumps({
            'first_name': 'Martin',
            'last_name': 'Fowler',
            'location': 'Berlin, Germany',
            'avatar_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Webysther_20150414193208_'
                          '-_Martin_Fowler.jpg/220px-Webysther_20150414193208_-_Martin_Fowler.jpg',
            'additional_information': 'Software Engineer at Travis-CI.',
            'website_url': 'https://martinfowler.com',
            'linkedin_url': 'https://www.linkedin.com/in/martinfowler',
            'twitter_url': 'https://twitter.com/in/martinfowler',
            'medium_url': 'https://medium.com/in/@martinfowler',
            'github_url': 'https://github.com/in/martinfowler',
            'facebook_url': 'https://www.acebook.com/in/martinfowler',
            'telegram_url': 'https://t.me/martinfowler',
            'steemit_url': 'https://steemit.com/@martinfowler',
        }), HTTP_AUTHORIZATION='JWT ' + self.user_token, content_type='application/json')

        assert Profile.objects.get(user=self.user).first_name == 'Martin'
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_update_user_profile_without_deletion_rights(self):
        """
        Case: updating a user profile without deletion rights.
        Expect: user has no authority to update this user profile by specified username error message.
        """
        expected_result = {
            'error': 'User has no authority to update this user profile by specified username.',
        }

        response = self.client.post(
            '/user/john.smith/profile/', HTTP_AUTHORIZATION='JWT ' + self.user_token, content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code

    def test_get_user_profile(self):
        """
        Case: get user profile.
        Expect: information of the user profile is received.
        """
        expected_result = {
            'result': {
                'user': {
                    'id': 32,
                    'last_login': None,
                    'is_superuser': False,
                    'email': 'martin.fowler@gmail.com',
                    'username': 'martin.fowler',
                    'is_active': True,
                    'is_staff': False,
                },
                'user_id': 32,
                'first_name': 'John',
                'last_name': 'Smith',
                'location': 'Tokyo, Japan',
                'avatar_url': 'https://block-producers-directory.s3-us-west-2.amazonaws.com/'
                              'user/avatars/default-user-logotype.png',
                'additional_information': 'Senior Software Engineer at Yamaha.',
                'website_url': 'https://johnsmith.com',
                'linkedin_url': '',
                'twitter_url': '',
                'medium_url': '',
                'github_url': '',
                'facebook_url': '',
                'telegram_url': '',
                'steemit_url': '',
            },
        }

        response = self.client.get(f'/user/{self.username}/profile/', content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_get_user_by_non_existing_username(self):
        """
        Case: get user profile by non-existing username.
        Expect: user profile with specified username does not exist error message.
        """
        expected_result = {
            'error': 'User with specified username does not exist.',
        }

        response = self.client.get('/user/not.martin.fowler/profile/', content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
