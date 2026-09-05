"""Tests for the authentication controller"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

import jwt
from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient

import twitchrewards.services.authentication.jwt
from twitchrewards.config import settings
from twitchrewards.main import app
from twitchrewards.repository import get_user_by_name
from twitchrewards.services.authentication import AUTH_COOKIE_KEY
from twitchrewards.twitch import TwitchBadResponse, TwitchResponse, TwitchUserResponse
from twitchrewards.twitch.user import User


def _userFactory() -> User:
    return User("test", "http://foo.test")


@dataclass
class MockGetTwitchUserResponseSettings:
    """Data used for the mocked Twitch API call"""

    is_twitch_response_successful: bool = True
    twitch_user: User = field(default_factory=_userFactory)


@dataclass
class MockGetTwitchAccessTokenSettings:
    """Data used for the mocked Twitch API call"""

    should_succeed: bool = True


client = TestClient(app, follow_redirects=False)
mock_get_user_data = MockGetTwitchUserResponseSettings()
mock_get_access_token_data = MockGetTwitchAccessTokenSettings()


def mock_get_twitch_user(_: str) -> TwitchResponse:
    """
    Mock the Twitch API call. Use MockGetTwitchUserNameSettings
    to customize the returned values.
    """
    if not mock_get_user_data.is_twitch_response_successful:
        return TwitchBadResponse()

    return TwitchUserResponse(mock_get_user_data.twitch_user)


def mock_get_twitch_access_token(_: str) -> Optional[str]:
    """
    Mock the Twitch API call. Use MockGetTwitchAccessTokenSettings
    to customize the returned values.
    """
    return "mock" if mock_get_access_token_data.should_succeed else None


def test_token_sets_jwt_for_user(monkeypatch: MonkeyPatch):
    """Test if the authentication generates the expected token"""
    twitch_name = "test"
    twitch_profile_user_url = "http://bar.test"
    twitch_user = User(twitch_name, twitch_profile_user_url)
    given_twitch_request_is_successful(monkeypatch, twitch_user)
    given_access_token_creation_succeeds(monkeypatch)

    response = client.post("token", json={"code": "code"})

    assert response.status_code == 200

    assert AUTH_COOKIE_KEY in client.cookies
    cookie = str(client.cookies[AUTH_COOKIE_KEY])[1:-1]
    assert cookie.startswith("Bearer ")
    access_token = cookie.split("Bearer ")[1]
    decoded_token = jwt.decode(
        access_token, settings.JWT_ENCODING_KEY, settings.JWT_ENCODING_ALGORITHM
    )
    assert "twitch_name" in decoded_token
    assert decoded_token["twitch_name"] == twitch_name
    assert "exp" in decoded_token
    assert datetime.fromtimestamp(decoded_token["exp"], timezone.utc) > datetime.now(
        timezone.utc
    )


def test_if_user_does_not_exist_should_create_user(monkeypatch: MonkeyPatch):
    """Test if a new user is being created when token is valid but there is no user"""
    twitch_name = str(uuid.uuid4())
    twitch_profile_user_url = "http://bar.test"
    twitch_user = User(twitch_name, twitch_profile_user_url)
    given_twitch_request_is_successful(monkeypatch, twitch_user)
    given_access_token_creation_succeeds(monkeypatch)

    response = client.post("token", json={"code": "dummy_code"})

    assert response.status_code == 200

    user = get_user_by_name(twitch_name)
    assert user is not None
    assert user.name == twitch_name
    assert user.profile_image_url == twitch_profile_user_url


def test_token_when_could_not_fetch_user_returns_unauthorized(monkeypatch: MonkeyPatch):
    """Test if the route returns 401 if the Twitch API call fails"""
    given_twitch_request_failed(monkeypatch)

    response = client.post("token", json={"code": "dummy_code"})

    assert response.status_code == 401


def test_token_when_could_not_fetch_access_token_returns_unauthorized(
    monkeypatch: MonkeyPatch,
):
    """Test if the route returns 401 if the Twitch API call fails"""
    twitch_name = str(uuid.uuid4())
    twitch_profile_user_url = "http://bar.test"
    twitch_user = User(twitch_name, twitch_profile_user_url)
    given_twitch_request_is_successful(monkeypatch, twitch_user)
    given_access_token_creation_fails(monkeypatch)

    response = client.post("token", json={"code": "dummy_code"})

    assert response.status_code == 401


def test_logout_should_remove_cookie():
    """Test if the route that logs out removes cookies"""
    client.cookies.set(AUTH_COOKIE_KEY, "dummy_value")

    try:
        response = client.get("logout")

        assert response.status_code == 200
        assert AUTH_COOKIE_KEY not in response.cookies
    finally:
        client.cookies.clear()


def given_twitch_request_is_successful(monkeypatch: MonkeyPatch, twitch_user: User):
    """
    Set Twitch API mock to return a successful request.

    Parameters:
        monkeypatch (MonkeyPatch): helper class to set up the mock.
        twitch_name (str): the name of the user in Twitch.
    """
    monkeypatch.setattr(
        twitchrewards.services.authentication.jwt,
        "get_twitch_user",
        mock_get_twitch_user,
    )

    mock_get_user_data.is_twitch_response_successful = True
    mock_get_user_data.twitch_user = twitch_user


def given_twitch_request_failed(monkeypatch: MonkeyPatch):
    """
    Set Twitch API mock to return a bad request.

    Parameters:
        monkeypatch (MonkeyPatch): helper class to set up the mock.
    """
    monkeypatch.setattr(
        twitchrewards.services.authentication.jwt,
        "get_twitch_user",
        mock_get_twitch_user,
    )

    mock_get_user_data.is_twitch_response_successful = False


# Those should likely be fixtures
def given_access_token_creation_succeeds(monkeypatch: MonkeyPatch):
    """
    Set Twitch API mock to return a token when creating an access token from code.

    Parameters:
        monkeypatch (MonkeyPatch): helper class to set up the mock.
    """
    monkeypatch.setattr(
        twitchrewards.services.authentication.jwt,
        "get_access_token",
        mock_get_twitch_access_token,
    )

    mock_get_access_token_data.should_succeed = True


def given_access_token_creation_fails(monkeypatch: MonkeyPatch):
    """
    Set Twitch API mock to return a bad request when creating an access token from code.

    Parameters:
        monkeypatch (MonkeyPatch): helper class to set up the mock.
    """
    monkeypatch.setattr(
        twitchrewards.services.authentication.jwt,
        "get_access_token",
        mock_get_twitch_access_token,
    )

    mock_get_access_token_data.should_succeed = False
