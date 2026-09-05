"""Tests for the profile controller"""

import uuid

from fastapi.testclient import TestClient

from tests.helpers import given_user
from twitchrewards.main import app

client = TestClient(app)


def test_should_return_user_profile():
    """Test if profile is returned correctly"""
    user_name = str(uuid.uuid4())
    given_user(user_name)

    response = client.get(f"/profiles/{user_name}")
    assert response.status_code == 200

    assert user_name in response.text


def test_when_user_does_not_exists_should_404():
    """Test if profile returns 404 is user does not exist"""
    user_name = str(uuid.uuid4())

    response = client.get(f"/profiles/{user_name}")
    assert response.status_code == 404
