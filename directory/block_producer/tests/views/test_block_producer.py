"""
Provide tests for implementation of block producer endpoints.
"""
import json
from http import HTTPStatus

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
            name='Block producer Spain',
            website_url='https://bpspain.com',
            short_description='Founded by a team of serial tech entrepreneurs in Spain.',
        )

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'username_or_email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        self.user_token = response.data.get('token')

    def test_get_block_producer(self):
        """
        Case: get block producer.
        Expect: information of the block producer is returned.
        """
        expected_result = {
            'result': {
                'user': {
                    'id': 6,
                    'last_login': None,
                    'is_superuser': False,
                    'email': 'martin.fowler@gmail.com',
                    'username': 'martin.fowler',
                    'is_active': True,
                    'is_staff': False,
                },
                'user_id': 6,
                'id': 12,
                'name': 'Block producer Canada',
                'website_url': 'https://bpcanada.com',
                'short_description': 'Founded by a team of serial tech entrepreneurs in Canada.',
                'location': '',
                'full_description': '',
                'logo_url': 'https://block-producers-directory.s3-us-west-2.amazonaws.com/'
                            'bps/logos/default-block-producer-logotype.png',
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

        response = self.client.get('/block-producers/12/', content_type='application/json')

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
        assert HTTPStatus.BAD_REQUEST == response.status_code

    def test_update_block_producer(self):
        """
        Case: update block producer with specified information.
        Expect: block producer updated in the database.
        """
        expected_result = {
            'result': 'Block producer has been updated.',
        }

        block_producer_identifier = 17

        BLOCK_PRODUCER_INFO.update(name='Block producer Japan')

        response = self.client.post(
            f'/block-producers/{block_producer_identifier}/',
            json.dumps(BLOCK_PRODUCER_INFO),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert BlockProducer.objects.get(id=block_producer_identifier).name == 'Block producer Japan'
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
        expected_result = {
            'result': 'Block producer has been created.',
        }

        response = self.client.put(
            '/block-producers/',
            json.dumps(BLOCK_PRODUCER_INFO),
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert BlockProducer.objects.get(id=3).name == 'Block producer USA'
        assert expected_result == response.json()
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
