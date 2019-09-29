"""
Provide tests for implementation of block producer endpoints.
"""
import json
from http import HTTPStatus
from unittest.mock import patch

from django.test import TestCase

from block_producer.models import BlockProducer
from user.models import User

BLOCK_PRODUCER_INFO = {
    'name': 'Block producer USA',
    'website_url': 'https://bpusa.com',
    'location': 'San Francisco, USA',
    'short_description': 'Leading Block Producer - founded by a team of '
                         'serial tech entrepreneurs, headquartered in USA',
    'full_description': '# About Us\n\nFounded by a team of serial tech entrepreneurs, '
                        'block producer USA is headquartered in San Francisco, USA and '
                        'is backed by reputable American financial players. We believe '
                        'that BP.IO will fundamentally change our economic and social '
                        'systems and as such we are deeply committed to contribute to '
                        'the growth of the ecosystem.',
    'logo_url': '',
    'linkedin_url': 'https://www.linkedin.com/in/bpusa',
    'twitter_url': 'https://twitter.com/bpusa',
    'medium_url': 'https://medium.com/@bpusa',
    'github_url': 'https://github.com/bpusa',
    'facebook_url': 'https://www.facebook.com/bpusa',
    'telegram_url': 'https://t.me/bpusa',
    'reddit_url': 'https://reddit.com/@bpusa',
    'slack_url': 'https://slack.com/bpusa',
    'wikipedia_url': 'https://wikipedia.com/bpusa',
    'steemit_url': 'https://steemit.com/@bpusa',
}


class TestBlockProducerSingle(TestCase):
    """
    Implements tests for implementation of single block producer endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.user = User.objects.create_user(
            id=1,
            email='martin.fowler@gmail.com',
            username='martin.fowler',
            password='martin.fowler.1337',
        )

        BlockProducer.objects.create(
            id=1,
            user=self.user,
            name='Block producer Canada',
            website_url='https://bpcanada.com',
            short_description='Founded by a team of serial tech entrepreneurs in Canada.',
        )

        BlockProducer.objects.create(
            id=2,
            user=self.user,
            name='Block producer Spain',
            website_url='https://bpspain.com',
            short_description='Founded by a team of serial tech entrepreneurs in Spain.',
        )

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'username_or_email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        self.user_token = response.data.get('token')

        self.second_user = User.objects.create_user(
            id=2,
            email='john.cap@gmail.com',
            username='john.cap',
            password='john.cap.1337',
        )

        BlockProducer.objects.create(
            id=4,
            user=self.second_user,
            name='Remme',
            website_url='https://remmebp.com',
            short_description='Founded by a team of serial tech entrepreneurs in Ukraine.',
        )

    def test_get_block_producer(self):
        """
        Case: get block producer.
        Expect: information of the block producer is returned.
        """
        expected_result = {
            'result': {
                'user': {
                    'id': 1,
                    'last_login': None,
                    'is_superuser': False,
                    'email': 'martin.fowler@gmail.com',
                    'username': 'martin.fowler',
                    'is_active': True,
                    'is_staff': False,
                },
                'user_id': 1,
                'id': 1,
                'name': 'Block producer Canada',
                'website_url': 'https://bpcanada.com',
                'short_description': 'Founded by a team of serial tech entrepreneurs in Canada.',
                'location': '',
                'full_description': '',
                'logo_url': 'https://block-producers-directory.s3-us-west-2.amazonaws.com/'
                            'bps/logos/default-block-producer-logotype.png',
                'status': 'moderation',
                'status_description': '',
                'linkedin_url': '',
                'twitter_url': '',
                'medium_url': '',
                'github_url': '',
                'facebook_url': '',
                'telegram_url': '',
                'reddit_url': '',
                'slack_url': '',
                'wikipedia_url': '',
                'steemit_url': '',
            },
        }

        response = self.client.get('/block-producers/1/', content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_get_block_producer_by_non_exiting_identifier(self):
        """
        Case: get block producer by non-exiting identifier.
        Expect: block producer with specified identifier does not exist error message.
        """
        expected_result = {
            'error': 'Block producer with specified identifier does not exist.',
        }

        non_existing_block_producer_identifier = 100500

        response = self.client.get(
            f'/block-producers/{non_existing_block_producer_identifier}/', content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_update_block_producer(self):
        """
        Case: update block producer with specified information.
        Expect: block producer updated in the database.
        """
        expected_result = {
            'result': 'Block producer has been updated.',
        }

        BLOCK_PRODUCER_INFO.update(name='Block producer Japan')

        response = self.client.post(
            f'/block-producers/1/',
            json.dumps(BLOCK_PRODUCER_INFO),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert BlockProducer.objects.get(id=1).name == 'Block producer Japan'
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_update_block_producer_by_non_exiting_identifier(self):
        """
        Case: update block producer by non-exiting identifier.
        Expect: block producer with specified identifier does not exist error message.
        """
        expected_result = {
            'error': 'Block producer with specified identifier does not exist.',
        }

        non_existing_block_producer_identifier = 100500

        response = self.client.post(
            f'/block-producers/{non_existing_block_producer_identifier}/',
            json.dumps(BLOCK_PRODUCER_INFO),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_delete_block_producer(self):
        """
        Case: delete block producer by its identifier.
        Expect: block producer deleted from the database.
        """
        expected_result = {
            'result': 'Block producer has been deleted.',
        }

        response = self.client.delete(
            f'/block-producers/1/',
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_delete_block_producer_by_non_exiting_identifier(self):
        """
        Case: delete block producer by non-exiting identifier.
        Expect: block producer with specified identifier does not exist error message.
        """
        expected_result = {
            'error': 'Block producer with specified identifier does not exist.',
        }

        non_existing_block_producer_identifier = 100500

        response = self.client.delete(
            f'/block-producers/{non_existing_block_producer_identifier}/',
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_delete_block_producer_without_deletion_rights(self):
        """
        Case: deleting a block producer without deletion rights.
        Expect: user has no authority to delete this block producer by its identifier error message.
        """
        expected_result = {
            'error': 'User has no authority to delete this block producer by its identifier.',
        }

        response = self.client.delete(
            f'/block-producers/4/',
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code


class TestBlockProducerCollection(TestCase):
    """
    Implements tests for implementation of collection block producer endpoint.
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

        BlockProducer.objects.create(
            user=self.user,
            name='Block producer Canada',
            website_url='https://bpcanada.com',
            short_description='Founded by a team of serial tech entrepreneurs in Canada.',
        )

        BlockProducer.objects.create(
            user=self.user,
            name='Block producer United Kingdom',
            website_url='https://bpunitedkingdom.com',
            short_description='Founded by a team of serial tech entrepreneurs in United Kingdom.',
        )

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'username_or_email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        self.user_token = response.data.get('token')

    def test_get_block_producers(self):
        """
        Case: get block producers.
        Expect: list of block producers is returned.
        """
        expected_result = {
            'result': [
                {
                    'website_url': 'https://bpunitedkingdom.com',
                    'medium_url': '',
                    'facebook_url': '',
                    'name': 'Block producer United Kingdom',
                    'twitter_url': '',
                    'short_description': 'Founded by a team of serial tech entrepreneurs in United Kingdom.',
                    'full_description': '',
                    'github_url': '',
                    'telegram_url': '',
                    'slack_url': '',
                    'wikipedia_url': '',
                    'user_id': 3,
                    'reddit_url': '',
                    'location': '',
                    'id': 7,
                    'linkedin_url': '',
                    'steemit_url': '',
                    'logo_url': 'https://block-producers-directory.s3-us-west-2.amazonaws.com/'
                                'bps/logos/default-block-producer-logotype.png',
                    'status': 'moderation',
                    'status_description': '',
                    'user': {
                        'is_staff': False,
                        'is_superuser': False,
                        'last_login': None,
                        'username': 'martin.fowler',
                        'email': 'martin.fowler@gmail.com',
                        'id': 3,
                        'is_active': True,
                    },
                },
                {
                    'website_url': 'https://bpcanada.com',
                    'medium_url': '',
                    'facebook_url': '',
                    'name': 'Block producer Canada',
                    'twitter_url': '',
                    'short_description': 'Founded by a team of serial tech entrepreneurs in Canada.',
                    'full_description': '',
                    'github_url': '',
                    'telegram_url': '',
                    'slack_url': '',
                    'wikipedia_url': '',
                    'user_id': 3,
                    'reddit_url': '',
                    'location': '',
                    'id': 6,
                    'linkedin_url': '',
                    'steemit_url': '',
                    'logo_url': 'https://block-producers-directory.s3-us-west-2.amazonaws.com/'
                                'bps/logos/default-block-producer-logotype.png',
                    'status': 'moderation',
                    'status_description': '',
                    'user': {
                        'is_staff': False,
                        'is_superuser': False,
                        'last_login': None,
                        'username': 'martin.fowler',
                        'email': 'martin.fowler@gmail.com',
                        'id': 3,
                        'is_active': True,
                    },
                },
            ],
        }

        response = self.client.get('/block-producers/', content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_create_block_producer(self):
        """
        Case: create block producer with specified information.
        Expect: block producer created in the database.
        """
        response = self.client.put(
            '/block-producers/',
            json.dumps(BLOCK_PRODUCER_INFO),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert BlockProducer.objects.get(id=3).name == 'Block producer USA'
        assert HTTPStatus.OK == response.status_code

    def test_create_block_producer_without_mandatory_argument(self):
        """
        Case: create block producer without mandatory argument.
        Expect: field name is required error message.
        """
        expected_result = {
            'errors': {
                'name': ['This field is required.'],
            },
        }

        del BLOCK_PRODUCER_INFO['name']

        response = self.client.put(
            '/block-producers/',
            json.dumps(BLOCK_PRODUCER_INFO),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code


class TestBlockProducerSearchCollection(TestCase):
    """
    Implements tests for implementation of collection search block producers endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        user = User.objects.create_user(
            email='martin.fowler@gmail.com',
            username='martin.fowler',
            password='martin.fowler.1337',
        )

        BlockProducer.objects.create(
            user=user,
            name='Block producer Canada',
            website_url='https://bpcanada.com',
            short_description='Founded by a team of serial tech entrepreneurs in Canada.',
        )

        BlockProducer.objects.create(
            user=user,
            name='Block producer USA',
            website_url='https://bpusa.com',
            short_description='Founded by a team of serial tech entrepreneurs in USA.',
        )

    def test_search_block_producers(self):
        """
        Case: search block producers by phrase.
        Expect: list of block producers is returned.
        """
        expected_result = {
            'result': [
                {
                    'website_url': 'https://bpusa.com',
                    'name': 'Block producer USA',
                    'facebook_url': '',
                    'location': '',
                    'telegram_url': '',
                    'id': 9,
                    'user_id': 4,
                    'github_url': '',
                    'slack_url': '',
                    'short_description': 'Founded by a team of serial tech entrepreneurs in USA.',
                    'user': {
                        'is_active': True,
                        'id': 4,
                        'email': 'martin.fowler@gmail.com',
                        'last_login': None,
                        'is_superuser': False,
                        'is_staff': False,
                        'username': 'martin.fowler',
                    },
                    'medium_url': '',
                    'reddit_url': '',
                    'wikipedia_url': '',
                    'steemit_url': '',
                    'linkedin_url': '',
                    'twitter_url': '',
                    'full_description': '',
                    'logo_url': 'https://block-producers-directory.s3-us-west-2.amazonaws.com/'
                                'bps/logos/default-block-producer-logotype.png',
                    'status': 'moderation',
                    'status_description': '',
                },
            ],
        }

        response = self.client.get('/block-producers/search/?phrase=producer%usa', content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_search_block_producers_by_non_existent_phrase(self):
        """
        Case: search block producers by non-existent phrase.
        Expect: empty list of block producers is returned.
        """
        expected_result = {'result': []}

        response = self.client.get('/block-producers/search/?phrase=queen', content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code


class TestRejectedBlockProducerDescriptionSingle(TestCase):
    """
    Implements tests for implementation of single rejected block producer description endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.email = 'martin.fowler@gmail.com'

        user = User.objects.create_user(
            email=self.email,
            username='martin.fowler',
            password='martin.fowler.1337',
        )

        BlockProducer.objects.create(
            user=user,
            name='Block producer USA',
            website_url='https://bpusa.com',
            short_description='Founded by a team of serial tech entrepreneurs in USA.',
        )

    @patch('services.email.Email.send')
    def test_rejected_block_producer_description(self, mock_email_send):
        """
        Case: send block producer status description to the email address.
        Expect: message was sent to the specified email is returned.
        """
        block_producer = BlockProducer.objects.filter(user__email=self.email, id=12).values().first()

        if block_producer.get('status_description'):
            expected_result = {
                'result': 'Message was sent to the specified email address with a description '
                          'of the reason for the rejection of the block producer.',
            }

        else:
            expected_result = {
                'result': 'Block producer not rejected.',
            }

        mock_email_send.return_value = None

        response = self.client.post(
            '/block-producers/12/description/', json.dumps({'email': self.email}), content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_rejected_block_producer_description_with_incorrect_email(self):
        """
        Case: send block producer status description by incorrect email.
        Expect: enter a valid email address error message.
        """
        expected_result = {
            'errors': {
                'email': ['Enter a valid email address.'],
            },
        }

        response = self.client.post('/block-producers/12/description/', json.dumps({
            'email': 'martin.fowler.1337',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code

    def test_rejected_block_producer_description_with_non_existent_email(self):
        """
        Case: send block producer status description with non-existent email.
        Expect: user with specified e-mail address does not exist error message.
        """
        expected_result = {
            'error': 'User with specified e-mail address does not exist.',
        }

        response = self.client.post('/block-producers/12/description/', json.dumps({
            'email': 'flower@gmail.com',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_rejected_block_producer_description_without_email(self):
        """
        Case: send block producer status description without email.
        Expect: this field is required error message.
        """
        expected_result = {
            'errors': {
                'email': ['This field is required.'],
            },
        }

        response = self.client.post(
            '/block-producers/12/description/', json.dumps({}), content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code

    def test_rejected_block_producer_description_by_non_exiting_identifier(self):
        """
        Case: send block producer status description by non-exiting identifier.
        Expect: block producer with specified identifier does not exist error message.
        """
        expected_result = {
            'error': 'Block producer with specified identifier does not exist.',
        }

        non_existing_block_producer_identifier = 100500

        response = self.client.post(
            f'/block-producers/{non_existing_block_producer_identifier}/description/',
            json.dumps({'email': self.email}),
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.NOT_FOUND == response.status_code
