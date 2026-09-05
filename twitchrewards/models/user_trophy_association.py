"""SQLAlchemy functions to define the relationship between users and trophies"""

from sqlalchemy import Column, ForeignKey, Table

from twitchrewards.models.base_db_model import Base

_users_trophies_table = Table(
    "UsersTrophies",
    Base.metadata,
    Column("UserId", ForeignKey("Users.Id")),
    Column("TrophyId", ForeignKey("Trophies.Id")),
)
