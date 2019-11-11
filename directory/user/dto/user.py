"""
Provide implementation of user data transfer object.
"""
import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class UserDto:
    """
    User data transfer object implementation.
    """

    id: typing.Any
    email: str
    username: str
    is_email_confirmed: bool
    is_active: bool
    is_staff: bool
    is_superuser: bool
    last_login: typing.Any = None


@dataclass_json
@dataclass
class UserDtoWithoutEmail:
    """
    User data transfer object without email field implementation.
    """

    id: typing.Any
    username: str
    is_email_confirmed: bool
    is_active: bool
    is_staff: bool
    is_superuser: bool
    last_login: typing.Any = None
