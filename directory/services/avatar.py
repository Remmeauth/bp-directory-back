"""
Provide implementation of avatar.
"""
from enum import (
    Enum,
    auto,
)

import boto3
from django.conf import settings


class AvatarTypes(Enum):
    """
    Provide avatar types.
    """

    block_producer = auto()
    user = auto()


class Avatar:
    """
    Avatar implementation.
    """

    def __init__(self, name, type_):
        """
        Constructor.
        """
        if type_ == AvatarTypes.user:
            self.path_to_store = f'users/avatars/{name}.png'

        if type_ == AvatarTypes.block_producer:
            self.path_to_store = f'bps/logos/{name}.png'

        self.aws_s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def get_url(self):
        """
        Get URL of uploaded avatar.
        """
        bucket_location = self.aws_s3.get_bucket_location(Bucket=settings.AWS_BUCKET_NAME).get('LocationConstraint')
        return f'https://s3-{bucket_location}.amazonaws.com/{settings.AWS_BUCKET_NAME}/{self.path_to_store}'

    def upload(self, file_object):
        """
        Upload avatar and make public.
        """
        self.aws_s3.put_object(
            Bucket=settings.AWS_BUCKET_NAME,
            Key=self.path_to_store,
            Body=file_object,
            ContentType='image/png',
        )

        self.aws_s3.put_object_acl(
            Bucket=settings.AWS_BUCKET_NAME,
            Key=self.path_to_store,
            ACL='public-read',
        )
