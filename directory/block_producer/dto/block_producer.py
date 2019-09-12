"""
Provide implementation of block producer data transfer object.
"""
import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from user.dto.user import UserDto


@dataclass_json
@dataclass
class BlockProducerDto:
    """
    Block producer data transfer object implementation.
    """

    user: UserDto

    user_id: int
    id: int

    name: str
    website_url: str
    short_description: str
    created_at: typing.Any

    location: str = ''
    full_description: str = ''
    logo_url: str = ''
    status: str = ''

    linkedin_url: str = ''
    twitter_url: str = ''
    medium_url: str = ''
    github_url: str = ''
    facebook_url: str = ''
    telegram_url: str = ''
    reddit_url: str = ''
    slack_url: str = ''
    wikipedia_url: str = ''
    steemit_url: str = ''
