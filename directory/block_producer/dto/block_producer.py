"""
Provide implementation of block producer data transfer object.
"""
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BlockProducerDto:
    """
    Block producer data transfer object implementation.
    """

    user_id: int
    id: int

    name: str
    website_url: str
    short_description: str

    location: str = ''
    full_description: str = ''
    logo_url: str = ''

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
