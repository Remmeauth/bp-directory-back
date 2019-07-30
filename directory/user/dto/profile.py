"""
Provide implementation of user profile data transfer object.
"""
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from user.dto.user import UserDto


@dataclass_json
@dataclass
class UserProfileDto:
    """
    User profile data transfer object implementation.
    """

    user: UserDto

    user_id: int

    first_name: str = ''
    last_name: str = ''
    location: str = ''
    avatar_url: str = ''
    additional_information: str = ''

    website_url: str = ''
    linkedin_url: str = ''
    twitter_url: str = ''
    medium_url: str = ''
    github_url: str = ''
    facebook_url: str = ''
    telegram_url: str = ''
    steemit_url: str = ''
