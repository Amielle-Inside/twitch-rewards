"""Contains routes related to the user"""

from typing import Annotated, List, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import BaseModel

from twitchrewards.controllers.view_models import (
    UpdatePronounsData,
    UserViewModel,
    get_name_with_title,
)
from twitchrewards.models import Pronouns, User
from twitchrewards.repository import (
    get_user_by_name,
    update_active_trophies,
    update_user,
)
from twitchrewards.services.authentication import get_current_user

router = APIRouter()

MAX_ACTIVE_TROPHIES: int = 3


class SetActiveTrophiesBody(BaseModel):
    trophies_ids: List[int]


@router.get("/{user_name}", status_code=status.HTTP_200_OK)
def fetch_user_metadata(user_name: str):
    """Gets metadata of a user to display in chat"""
    user = get_user_by_name(user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return parse(user)


@router.get("", status_code=status.HTTP_200_OK)
def fetch_current_user(user: Annotated[Optional[User], Depends(get_current_user)]):
    """Fetches the current user base on the current JWT"""
    if not user:
        raise HTTPException(status_code=404, detail="No user authenticated")

    return parse(user)


@router.post("/active-trophies", status_code=status.HTTP_200_OK)
def set_active_trophies(
    body: SetActiveTrophiesBody,
    user: Annotated[Optional[User], Depends(get_current_user)],
):
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    if len(body.trophies_ids) > MAX_ACTIVE_TROPHIES:
        raise HTTPException(
            status_code=403,
            detail=f"Max active trophies ({MAX_ACTIVE_TROPHIES}) exceeded",
        )

    user_trophies_ids = [trophy.id for trophy in user.trophies]
    valid_trophies = [
        trophy_id for trophy_id in body.trophies_ids if trophy_id in user_trophies_ids
    ]
    user_owns_all_trophies = len(valid_trophies) == len(body.trophies_ids)
    if not user_owns_all_trophies:
        raise HTTPException(
            status_code=403, detail="User does not own all requested trophies"
        )

    update_active_trophies(user.id, body.trophies_ids)


@router.post("/set-pronouns", status_code=status.HTTP_200_OK)
def update_pronouns(
    pronouns: UpdatePronounsData,
    user: Annotated[Optional[User], Depends(get_current_user)],
):
    """Updates the pronouns of the current user"""
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    user.pronouns = pronouns.pronouns
    update_user(user)


def parse_pronouns(pronoun: Pronouns) -> str:
    """
    Return the localized string representation of the pronoun.

    Parameters:
        pronoun (Pronouns): Pronoun to parse.

    Returns:
        str: Localized string representation of the pronoun.
    """
    if pronoun == Pronouns.HE:
        return "ele/dele"
    if pronoun == Pronouns.SHE:
        return "ela/dela"
    if pronoun == Pronouns.THEY:
        return "elu/delu"
    if pronoun == Pronouns.ALL:
        return "todos pronomes"
    return ""


def parse(user: User) -> UserViewModel:
    """
    Return the view model representation of the user. Enums are parsed
    to their string representation.

    Parameters:
        user (User): User to be parsed.

    Returns:
        UserViewModel: Parsed user.
    """
    pronouns = parse_pronouns(user.pronouns)
    display_name = get_name_with_title(user.title, user.name, user.pronouns)
    return UserViewModel(
        display_name=display_name,
        pronouns=pronouns,
        pronouns_id=user.pronouns,
        trophies=user.trophies,
    )
