"""
Provide implementation of user data transfer object.
"""
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class UserDto:
    """
    User data transfer object implementation.
    """

    id: str
    email: str
    username: str
    last_login: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
