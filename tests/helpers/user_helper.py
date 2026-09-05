from datetime import datetime
from typing import Optional

import jwt

from twitchrewards.config import settings
from twitchrewards.models import Pronouns, Title, User
from twitchrewards.repository import create_user, get_user_by_name


def given_user(
    name: str,
    pronouns: Pronouns = Pronouns.THEY,
    title: Title = Title.NONE,
    profile_image_url: str = "http://foo.test",
) -> User:
    """Insert a new user in the database."""

    create_user(
        User(
            name=name,
            pronouns=pronouns,
            title=title,
            profile_image_url=profile_image_url,
        )
    )
    return get_user_by_name(name)  # type: ignore


def given_valid_token(twitch_name: str, expires_at: Optional[datetime] = None):
    """Encodes a valid JWT token to authenticate in the application."""
    token_data = {
        "twitch_name": twitch_name,
    }
    if expires_at:
        token_data["exp"] = str(expires_at)

    return jwt.encode(
        token_data,
        settings.JWT_ENCODING_KEY,
        algorithm=settings.JWT_ENCODING_ALGORITHM,
    )
