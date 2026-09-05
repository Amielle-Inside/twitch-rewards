"""Returns a user profile. Not under user.py atm as that is currently an API"""

from fastapi import APIRouter, HTTPException, status
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from twitchrewards.repository import get_user_by_name

router = APIRouter()
templates = Jinja2Templates(directory="twitchrewards/views")


@router.get("/{user_name}", status_code=status.HTTP_200_OK)
def fetch_user_profile(request: Request, user_name: str):
    """Shows the user profile"""
    user = get_user_by_name(user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "user": user,
        },
    )
