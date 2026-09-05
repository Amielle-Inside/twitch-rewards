"""Contains the representation of a Twitch user"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship

from twitchrewards.models.base_db_model import Base
from twitchrewards.models.pronouns import Pronouns
from twitchrewards.models.sqlalchemy_enum_type import IntEnum
from twitchrewards.models.titles import Title
from twitchrewards.models.trophies.trophy import DbTrophy, Trophy
from twitchrewards.models.trophies.trophy_mapper import specific_trophy
from twitchrewards.models.user_trophy_association import _users_trophies_table


@dataclass
class User(Base):
    """
    Store data for a Twitch user. User are identified by name.
    Changing the name on Twitch requires an update here.
    """

    __tablename__ = "Users"

    id: int = Column(Integer, name="Id", primary_key=True)  # type: ignore
    name: str = Column(String, name="Name")  # type: ignore
    profile_image_url: str = Column(String, name="ProfileImageUrl")  # type: ignore
    pronouns: Pronouns = Column(IntEnum(Pronouns), name="Pronouns")  # type: ignore
    title: Title = Column(IntEnum(Title), name="Title")  # type: ignore
    _trophies: Mapped[List[DbTrophy]] = relationship(secondary=_users_trophies_table)  # type: ignore
    active_trophies_ids = Column(JSON, name="ActiveTrophies")

    @hybrid_property
    def trophies(self):
        return [specific_trophy(trophy) for trophy in self._trophies]

    def has_trophy(self, trophy_id: int) -> bool:
        return trophy_id in [trophy.id for trophy in self.trophies]
