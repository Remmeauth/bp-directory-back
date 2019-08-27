"""
Provide database models for block producer.
"""
from django.conf import settings
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
)
from django.db import models

from block_producer.dto.block_producer import BlockProducerDto
from user.models import User

BLOCK_PRODUCER_STATUS_MODERATION = 'moderation'
BLOCK_PRODUCER_STATUS_DECLINED = 'declined'
BLOCK_PRODUCER_STATUS_ACTIVE = 'active'

BLOCK_PRODUCER_STATUSES = (
    (BLOCK_PRODUCER_STATUS_MODERATION, BLOCK_PRODUCER_STATUS_MODERATION),
    (BLOCK_PRODUCER_STATUS_DECLINED, BLOCK_PRODUCER_STATUS_DECLINED),
    (BLOCK_PRODUCER_STATUS_ACTIVE, BLOCK_PRODUCER_STATUS_ACTIVE),
)


class BlockProducer(models.Model):
    """
    Block producer database model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, blank=False)
    website_url = models.URLField(max_length=200, blank=False)
    location = models.CharField(max_length=100, blank=True)
    short_description = models.CharField(max_length=100, blank=False)
    full_description = models.TextField(blank=True)
    logo_url = models.URLField(max_length=200, blank=True, default=settings.DEFAULT_BLOCK_PRODUCER_LOGOTYPE_URL)
    status = models.CharField(max_length=10, choices=BLOCK_PRODUCER_STATUSES, default=BLOCK_PRODUCER_STATUS_MODERATION)

    linkedin_url = models.URLField(max_length=200, blank=True)
    twitter_url = models.URLField(max_length=200, blank=True)
    medium_url = models.URLField(max_length=200, blank=True)
    github_url = models.URLField(max_length=200, blank=True)
    facebook_url = models.URLField(max_length=200, blank=True)
    telegram_url = models.URLField(max_length=200, blank=True)
    reddit_url = models.URLField(max_length=200, blank=True)
    slack_url = models.URLField(max_length=200, blank=True)
    wikipedia_url = models.URLField(max_length=200, blank=True)
    steemit_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        """
        Get string representation of an object.
        """
        return f'{self.name} — {self.user.email}'

    @classmethod
    def does_exist(cls, identifier):
        """
        Check if block producer exists by its identifier.
        """
        if cls.objects.filter(id=identifier).exists():
            return True

        return False

    @classmethod
    def get_all(cls):
        """
        Get block producers.
        """
        block_producers_as_dicts = cls.objects.all().values()

        for block_producer in block_producers_as_dicts:

            user_identifier = block_producer.get('user_id')
            user_as_dict = User.objects.filter(id=user_identifier).values().first()

            del user_as_dict['password']
            del user_as_dict['created']

            block_producer['user'] = user_as_dict

        return BlockProducerDto.schema().load(block_producers_as_dicts, many=True)

    @classmethod
    def create(cls, email, info):
        """
        Create a block producer with specified information.
        """
        user = User.objects.get(email=email)

        if not info.get('logo_url'):
            del info['logo_url']

        cls.objects.create(user=user, **info)

    @classmethod
    def update(cls, email, identifier, info):
        """
        Update block producer with specified information.
        """
        user = User.objects.get(email=email)
        cls.objects.filter(user=user, id=identifier).update(**info)

    @classmethod
    def get(cls, identifier):
        """
        Get block producer by its identifier.
        """
        block_producer_as_dict = cls.objects.filter(id=identifier).values().first()

        user_identifier = block_producer_as_dict.get('user_id')
        user_as_dict = User.objects.filter(id=user_identifier).values().first()

        del user_as_dict['password']
        del user_as_dict['created']

        block_producer_as_dict['user'] = user_as_dict

        return BlockProducerDto(**block_producer_as_dict)

    @classmethod
    def search(cls, phrase):
        """
        Search block producers by phrase.
        """
        search_vector = SearchVector('name', weight='A') + \
            SearchVector('location', weight='B') + \
            SearchVector('short_description', weight='B') + \
            SearchVector('full_description', weight='B')

        block_producers_as_list = cls.objects.annotate(
            search=search_vector,
        ).filter(search=SearchQuery(phrase)).values()

        for block_producer_as_dict in block_producers_as_list:
            user_identifier = block_producer_as_dict.get('user_id')

            user_as_dict = User.objects.filter(id=user_identifier).values().first()

            del user_as_dict['password']
            del user_as_dict['created']

            del block_producer_as_dict['search']

            block_producer_as_dict['user'] = user_as_dict

        return BlockProducerDto.schema().load(block_producers_as_list, many=True)

    @classmethod
    def get_last(cls, user_email):
        """
        Get user's last block producer by user's email.
        """
        block_producers_as_dict = cls.objects.filter(user__email=user_email)

        if not block_producers_as_dict:
            return None

        last_block_producer = block_producers_as_dict.values().last()

        user_identifier = last_block_producer.get('user_id')
        user_as_dict = User.objects.filter(id=user_identifier).values().first()

        del user_as_dict['password']
        del user_as_dict['created']

        last_block_producer['user'] = user_as_dict

        return BlockProducerDto(**last_block_producer)
