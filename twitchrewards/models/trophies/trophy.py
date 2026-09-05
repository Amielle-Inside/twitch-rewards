"""Contains the representation of a Trophy"""

from abc import ABC
from dataclasses import dataclass

from sqlalchemy import Boolean, Column, Integer

from twitchrewards.models.base_db_model import Base


@dataclass
class DbTrophy(Base):
    """
    Store data for a Trophy. A Trophy is a reward a user may claim.
    """

    __tablename__ = "Trophies"

    id: int = Column(Integer, name="Id", primary_key=True)  # type: ignore
    redeemable: bool = Column(Boolean, name="Redeemable")  # type: ignore


@dataclass(init=False)
class Trophy(ABC):
    id: int
    name: str
    description: str
    image_path: str
    redeemable: bool
