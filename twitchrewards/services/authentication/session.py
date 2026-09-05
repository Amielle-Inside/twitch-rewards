"""Module to access data for the current session"""

from typing import Annotated, Optional

import jwt
from fastapi import Cookie, Header

from twitchrewards.models import User
from twitchrewards.repository import get_user_by_name
from twitchrewards.services.authentication.jwt import decode

AUTH_COOKIE_KEY = "cookie_auth"


def get_current_user(
    authorization: Annotated[Optional[str], Header()] = None,
    cookie_auth: Annotated[Optional[str], Cookie()] = None,
) -> Optional[User]:
    """
    Get the current user given the token in the Authorization header or cookie.

    Parameters:
        authorization (str): Value of the authorization header.
        cookie_auth (str): Value of the authorization in the cookies.

    Returns:
        Optional[User]: The user matching the access token, if any.
    """
    authorization = authorization if authorization is not None else cookie_auth
    if not authorization or not authorization.startswith("Bearer "):
        return None

    split_token = authorization.split("Bearer ")
    token = split_token[1]
    try:
        name = decode(token)
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return None

    return get_user_by_name(name)
