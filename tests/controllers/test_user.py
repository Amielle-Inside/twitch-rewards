"""Tests for the user controller"""

import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from tests.helpers import given_user, given_valid_token
from twitchrewards.main import app
from twitchrewards.models import EarlyUser, Pronouns, Title, User
from twitchrewards.repository import add_trophy, get_user_by_name

client = TestClient(app)


@pytest.mark.parametrize(
    "pronouns,expected_description",
    [
        (Pronouns.UNKNOWN, ""),
        (Pronouns.HE, "ele/dele"),
        (Pronouns.SHE, "ela/dela"),
        (Pronouns.THEY, "elu/delu"),
        (Pronouns.ALL, "todos pronomes"),
    ],
)
def test_should_return_pronouns(pronouns: Pronouns, expected_description: str):
    """Test if pronouns are returned correctly"""
    user_name = str(uuid.uuid4())
    given_user(user_name, pronouns)

    response = client.get(f"/users/{user_name}")
    assert response.status_code == 200

    user = response.json()
    assert user["pronouns"] == expected_description
    assert user["pronouns_id"] == pronouns


def test_when_user_does_not_exists_should_return_404():
    """Test if pronouns are returned correctly"""
    user_name = str(uuid.uuid4())

    response = client.get(f"/users/{user_name}")

    assert response.status_code == 404


def test_when_user_does_not_have_title_should_return_name():
    """Test if the display name is returned when user has no title set"""
    user_name = str(uuid.uuid4())
    given_user(user_name)

    response = client.get(f"/users/{user_name}")
    assert response.status_code == 200

    user = response.json()
    assert user["display_name"] == user_name


@pytest.mark.parametrize(
    "pronouns",
    [
        Pronouns.UNKNOWN,
        Pronouns.HE,
        Pronouns.SHE,
        Pronouns.THEY,
        Pronouns.ALL,
    ],
)
def test_when_user_has_streamer_title_should_return_name(pronouns: Pronouns):
    """Test if pronouns are returned correctly"""
    user_name = str(uuid.uuid4())
    given_user(user_name, pronouns, title=Title.STREAMER)

    response = client.get(f"/users/{user_name}")
    assert response.status_code == 200

    user = response.json()
    assert user["display_name"] == f"Streamer {user_name}"


def test_when_updating_pronouns_and_jwt_token_is_valid_update_pronouns():
    """Test if API returns 401 when token is invalid"""
    user_name = str(uuid.uuid4())
    given_user(user_name, Pronouns.UNKNOWN)
    token = given_valid_token(user_name)

    response = client.post(
        "/users/set-pronouns",
        headers={"Authorization": f"Bearer {token}"},
        json={"pronouns": 2},
    )
    assert response.status_code == 200

    user = get_user_by_name(user_name)
    assert user.pronouns == Pronouns.SHE


def test_when_updating_pronouns_and_jwt_token_is_set_on_cookies_update_pronouns():
    """Test if API returns 401 when token is invalid"""
    user_name = str(uuid.uuid4())
    given_user(user_name, Pronouns.UNKNOWN)
    token = given_valid_token(user_name)

    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.post(
        "/users/set-pronouns",
        json={"pronouns": 2},
    )
    assert response.status_code == 200

    user = get_user_by_name(user_name)
    assert user.pronouns == Pronouns.SHE

    client.cookies.clear()


def test_when_updating_pronouns_and_jwt_token_is_invalid_returns_unauthorized():
    """Test if API returns 401 when token is invalid"""
    user_name = str(uuid.uuid4())
    given_user(user_name, Pronouns.UNKNOWN)
    token = "foo"

    response = client.post(
        "/users/set-pronouns",
        headers={"Authorization": f"Bearer {token}"},
        json={"pronouns": 2},
    )
    assert response.status_code == 401


def test_when_updating_pronouns_and_jwt_token_is_expired_returns_unauthorized():
    """Test if API returns 401 when token is expired"""
    user_name = str(uuid.uuid4())
    given_user(user_name, Pronouns.UNKNOWN)
    token_expire_date = datetime.now(timezone.utc) - timedelta(1)
    token = given_valid_token(user_name, expires_at=token_expire_date)

    response = client.post(
        "/users/set-pronouns",
        headers={"Authorization": f"Bearer {token}"},
        json={"pronouns": 2},
    )
    assert response.status_code == 401


def test_when_fetching_current_user_returns_user():
    """
    Test if API returns the current user in the current user route
    when the user is authenticated
    """
    user_name = str(uuid.uuid4())
    given_user(user_name, Pronouns.UNKNOWN)
    token = given_valid_token(user_name)

    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.get("/users")

    assert response.status_code == 200
    json = response.json()
    assert json["display_name"] == user_name

    client.cookies.clear()


def test_when_fetching_current_and_no_authenticated_user_returns_404():
    """Test if API returns 404 in the current user route if no user is authenticated"""
    user_name = str(uuid.uuid4())
    given_user(user_name, Pronouns.UNKNOWN)

    response = client.get("/users")

    assert response.status_code == 404


def test_when_user_has_trophies_returns_trophies():
    user_name = str(uuid.uuid4())
    user = given_user(user_name)
    trophy = EarlyUser(False)
    add_trophy(user, trophy)

    response = client.get(f"/users/{user_name}")
    assert response.status_code == 200

    user = response.json()
    assert len(user["trophies"]) == 1
    assert user["trophies"][0]["id"] == trophy.id


def test_set_active_trophies_sets_active_trophies():
    user_name = str(uuid.uuid4())
    user = given_user(user_name, Pronouns.UNKNOWN)
    trophy = EarlyUser(False)
    add_trophy(user, trophy)

    token = given_valid_token(user_name)
    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.post("/users/active-trophies", json={"trophies_ids": [1]})

    assert response.status_code == 200

    updated_user = get_user_by_name(user_name)
    assert updated_user.active_trophies_ids == [1]

    client.cookies.clear()


def test_set_active_trophies_when_no_user_returns_401():
    user_name = str(uuid.uuid4())
    user = given_user(user_name, Pronouns.UNKNOWN)
    trophy = EarlyUser(False)
    add_trophy(user, trophy)

    response = client.post("/users/active-trophies", json={"trophies_ids": [1]})

    assert response.status_code == 401

    updated_user = get_user_by_name(user_name)
    assert updated_user.active_trophies_ids == None


def test_set_active_trophies_when_more_than_three_trophies_returns_403():
    user_name = str(uuid.uuid4())
    user = given_user(user_name, Pronouns.UNKNOWN)
    trophy = EarlyUser(False)
    add_trophy(user, trophy)

    token = given_valid_token(user_name)
    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.post(
        "/users/active-trophies", json={"trophies_ids": [1, 2, 3, 4]}
    )

    assert response.status_code == 403

    updated_user = get_user_by_name(user_name)
    assert updated_user.active_trophies_ids == None

    client.cookies.clear()


def test_set_active_trophies_when_user_does_not_have_trophy_returns_403():
    user_name = str(uuid.uuid4())
    given_user(user_name, Pronouns.UNKNOWN)
    token = given_valid_token(user_name)

    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.post("/users/active-trophies", json={"trophies_ids": [1]})

    assert response.status_code == 403

    updated_user = get_user_by_name(user_name)
    assert updated_user.active_trophies_ids == None

    client.cookies.clear()
