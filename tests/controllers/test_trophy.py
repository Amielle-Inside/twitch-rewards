import uuid
from typing import Optional

import jwt
import pytest
from fastapi.testclient import TestClient

from tests.helpers import given_user, given_valid_token
from twitchrewards.main import app
from twitchrewards.models import EarlyUser
from twitchrewards.repository import (
    add_trophy,
    get_trophy_by_id,
    get_user_by_name,
    set_trophy_redeemable,
)

client = TestClient(app)


@pytest.mark.parametrize(
    "currently_redeemable,is_redeemable",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_set_redeemable_should_set_redeemable(
    currently_redeemable: bool, is_redeemable: bool
):
    trophy = EarlyUser(currently_redeemable)
    set_trophy_redeemable(trophy.id, currently_redeemable)

    response = client.post(
        f"/trophies/api/{trophy.id}/redeemable", json={"redeemable": is_redeemable}
    )
    assert response.status_code == 200

    updated_trophy = get_trophy_by_id(trophy.id)
    assert updated_trophy != None
    assert updated_trophy.redeemable == is_redeemable


def test_set_redeemable_when_trophy_does_not_exist_should_return_404():
    response = client.post(f"/trophies/api/12345/redeemable", json={"redeemable": True})

    assert response.status_code == 404


def test_redeem_trophy_redeems_trophy():
    set_trophy_redeemable(1, True)

    user_name = str(uuid.uuid4())
    given_user(user_name)
    token = given_valid_token(user_name)

    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.post("/trophies/api/1/redeem")
    assert response.status_code == 200

    user = get_user_by_name(user_name)
    assert len(user.trophies) == 1
    assert user.trophies[0].id == 1

    client.cookies.clear()


def test_redeem_trophy_when_no_logged_in_user_returns_404():
    set_trophy_redeemable(1, True)

    user_name = str(uuid.uuid4())
    given_user(user_name)
    token = given_valid_token(user_name)

    response = client.post("/trophies/api/1/redeem")
    assert response.status_code == 404

    user = get_user_by_name(user_name)
    assert len(user.trophies) == 0

    client.cookies.clear()


def test_redeem_trophy_when_trophy_does_not_exist_returns_404():
    set_trophy_redeemable(1, True)

    user_name = str(uuid.uuid4())
    given_user(user_name)
    token = given_valid_token(user_name)

    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.post("/trophies/api/12345/redeem")
    assert response.status_code == 404

    user = get_user_by_name(user_name)
    assert len(user.trophies) == 0

    client.cookies.clear()


def test_redeem_trophy_when_trophy_is_not_redeemable_returns_403():
    set_trophy_redeemable(1, False)

    user_name = str(uuid.uuid4())
    given_user(user_name)
    token = given_valid_token(user_name)

    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.post("/trophies/api/1/redeem")
    assert response.status_code == 403

    user = get_user_by_name(user_name)
    assert len(user.trophies) == 0

    client.cookies.clear()


def test_redeem_trophy_when_user_already_has_trophy_returns_200():
    trophy = EarlyUser(True)
    set_trophy_redeemable(trophy.id, True)

    user_name = str(uuid.uuid4())
    user = given_user(user_name)
    token = given_valid_token(user_name)

    add_trophy(user, trophy)

    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.post("/trophies/api/1/redeem")
    assert response.status_code == 200

    user = get_user_by_name(user_name)
    assert len(user.trophies) == 1

    client.cookies.clear()


def test_get_trophy_can_redeem_trophy():
    trophy = EarlyUser(True)
    set_trophy_redeemable(trophy.id, True)

    user_name = str(uuid.uuid4())
    user = given_user(user_name)
    token = given_valid_token(user_name)

    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.get("/trophies/1")
    assert response.status_code == 200

    assert "Resgatar" in response.text

    client.cookies.clear()


def test_get_trophy_when_trophy_was_redeemed_cannot_redeem():
    trophy = EarlyUser(True)
    set_trophy_redeemable(trophy.id, True)

    user_name = str(uuid.uuid4())
    user = given_user(user_name)
    token = given_valid_token(user_name)

    add_trophy(user, trophy)

    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.get("/trophies/1")
    assert response.status_code == 200

    assert "ja tem" in response.text

    client.cookies.clear()


def test_get_trophy_when_trophy_is_not_redeemable_cannot_redeem():
    trophy = EarlyUser(True)
    set_trophy_redeemable(trophy.id, False)

    user_name = str(uuid.uuid4())
    user = given_user(user_name)
    token = given_valid_token(user_name)

    client.cookies.set("cookie_auth", f"Bearer {token}")
    response = client.get("/trophies/1")
    assert response.status_code == 200

    assert "nao e mais resgatavel" in response.text

    client.cookies.clear()
