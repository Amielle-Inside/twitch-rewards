"""Contains routes related to authentication"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, Response

from twitchrewards.config import settings
from twitchrewards.controllers.view_models import AuthenticationData
from twitchrewards.services.authentication import (
    AUTH_COOKIE_KEY,
    authenticate_twitch_user,
)

router = APIRouter()


@router.get("/token")
def handle_twitch_redirect():
    """Sends user to a temporary page where we will post the Twitch token"""
    return FileResponse("twitchrewards/views/authenticate.html")


@router.post("/token", status_code=status.HTTP_200_OK)
def authenticate(authentication_data: AuthenticationData, response: Response):
    """Gets JWT to perform write operations in the API"""
    print(f"DEBUG: authenticate called with code={authentication_data.code[:10]}...")
    access_token = authenticate_twitch_user(authentication_data.code)
    print(f"DEBUG: authenticate_twitch_user returned: {access_token[:20] if access_token else None}...")
    if not access_token:
        raise HTTPException(status_code=401, detail="Unable to validate twitch token")

    # Use secure=False for HTTP, secure=True for HTTPS
    secure_cookie = settings.APP_HOST.startswith("https://")
    response.set_cookie(
        key=AUTH_COOKIE_KEY, 
        value=f"Bearer {access_token}", 
        httponly=True, 
        secure=secure_cookie, 
        samesite="lax"
    )
    print(f"DEBUG: Cookie set: {AUTH_COOKIE_KEY}, secure={secure_cookie}")


@router.get("/logout")
def logout():
    """Sends user to a temporary logout page"""
    return FileResponse("twitchrewards/views/logout.html")


@router.post("/logout")
def remove_auth_cookie(response: Response):
    """Removes the auth cookie form the user's browser"""
    response.delete_cookie(AUTH_COOKIE_KEY)
