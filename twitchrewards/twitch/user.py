"""The representation of a user returned by the Twitch API"""

from dataclasses import dataclass

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped

from twitchrewards.models.base_db_model import Base
from twitchrewards.models.pronouns import Pronouns
from twitchrewards.models.sqlalchemy_enum_type import IntEnum
from twitchrewards.models.titles import Title


@dataclass
class User:
    """
    A User retrieved from the Twitch API.
    """

    name: str
    profile_image_url: str
