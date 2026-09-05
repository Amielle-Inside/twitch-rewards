from typing import Optional

from sqlalchemy import update

from twitchrewards.models import DbTrophy, Trophy, specific_trophy
from twitchrewards.repository.database import get_db


def get_by_id(trophy_id: int) -> Optional[Trophy]:
    with get_db() as db:
        generic_trophy = db.query(DbTrophy).filter_by(id=trophy_id).first()
    return specific_trophy(generic_trophy) if generic_trophy else None


def set_redeemable(trophy_id: int, redeemable: bool):
    print(f"{trophy_id} - {redeemable}")
    stmt = (
        update(DbTrophy)
        .where(DbTrophy.id == trophy_id)  # type: ignore
        .values(redeemable=redeemable)
    )
    with get_db() as db:
        db.execute(stmt)
        db.commit()
