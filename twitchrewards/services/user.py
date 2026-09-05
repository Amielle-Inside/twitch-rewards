"""Orchestration layer for user management"""

from twitchrewards.models import Pronouns, Title, User
from twitchrewards.repository import create_user, get_user_by_name, update_user


def ensure_exists(user_name: str) -> User:
    """
    Creates a user with a given name, if one does not exist already.

    Parameters:
        user_name (str): Name of the user.
    """
    user = get_user_by_name(user_name)
    if not user:
        create_user(User(name=user_name, pronouns=Pronouns.UNKNOWN, title=Title.NONE))
        user = get_user_by_name(user_name)

    if not user:
        raise TypeError("User does not exist even after creation")

    return user
