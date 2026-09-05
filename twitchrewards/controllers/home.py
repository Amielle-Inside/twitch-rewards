"""For now this is acting as a catch all for the setting page"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from twitchrewards.config import settings
from twitchrewards.models import User
from twitchrewards.services.authentication import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="twitchrewards/views")


@router.get("/", status_code=status.HTTP_200_OK)
def home(request: Request, user: Annotated[Optional[User], Depends(get_current_user)]):
    """Allows user to change their personal data"""
    if not user:
        return RedirectResponse("/login")

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"user": user},
    )


@router.get("/login", status_code=status.HTTP_200_OK)
def login(request: Request):
    """Log in page"""
    # Build redirect_uri omitting default ports (80 for HTTP, 443 for HTTPS)
    # When behind Cloudflare Tunnel/reverse proxy, external port is always 443 (HTTPS) or 80 (HTTP)
    from urllib.parse import urlparse
    parsed = urlparse(settings.APP_HOST)
    # Use standard ports for redirect_uri since Cloudflare terminates SSL on 443
    if parsed.scheme == "https":
        redirect_uri = f"{settings.APP_HOST}/token"  # port 443 omitted
    elif parsed.scheme == "http":
        redirect_uri = f"{settings.APP_HOST}/token"  # port 80 omitted
    else:
        redirect_uri = f"{settings.APP_HOST}:{settings.APP_PORT}/token"
    
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "redirect_uri": redirect_uri,
            "client_id": settings.TWITCH_APP_CLIENT_ID,
        },
    )
