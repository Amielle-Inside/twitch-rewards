"""Used to interact with the User entity in the database"""

from typing import List, Optional

from sqlalchemy import text, update
from sqlalchemy.orm import joinedload

from twitchrewards.models import Trophy, User
from twitchrewards.repository.database import get_db


def get_by_name(name: str) -> Optional[User]:
    """
    Get a user with a given name.

    Parameters:
        name (str): Name of the user.

    Returns:
        User: User with the corresponding name.
    """
    with get_db() as db:
        return (
            db.query(User)
            .options(joinedload(User._trophies))
            .filter_by(name=name)
            .first()
        )


def update_user(user: User):
    """
    Update a user in the DB to match the given data.

    Parameters:
        user (User): User to update. It'll update data where using the Id for filtering.
    """
    stmt = (
        update(User)
        .where(User.id == user.id)  # type: ignore
        .values(
            pronouns=user.pronouns,
            title=user.title,
            profile_image_url=user.profile_image_url,
        )
    )
    with get_db() as db:
        db.execute(stmt)
        db.commit()


def update_profile_image_url(user_id: int, profile_image_url: str):
    """
    Update the profile image url of the given user.

    Parameters:
        user_id (int): Name of the user to update.
        profile_image_url(str): New profile image URL.
    """
    stmt = (
        update(User)
        .where(User.id == user_id)  # type: ignore
        .values(profile_image_url=profile_image_url)
    )
    with get_db() as db:
        db.execute(stmt)
        db.commit()


def create_user(user: User):
    """
    Adds a user to the DB.

    Parameters:
        user (User): User to be added.
    """
    with get_db() as db:
        db.add(user)
        db.commit()


def add_trophy(user: User, trophy: Trophy):
    """
    Adds a trophy to an user.

    Parameters:
        user (User): Owner of the trophy.
        trophy (Trophy): Trophy to be given.
    """
    with get_db() as db:
        db.execute(
            text(
                'INSERT INTO "UsersTrophies" ("UserId", "TrophyId") VALUES (:user_id, :trophy_id)'
            ),
            {"user_id": user.id, "trophy_id": trophy.id},
        )
        db.commit()


def update_active_trophies(user_id: int, active_trophies: List[int]):
    stmt = (
        update(User)
        .where(User.id == user_id)  # type: ignore
        .values(active_trophies_ids=active_trophies)
    )
    with get_db() as db:
        db.execute(stmt)
        db.commit()
