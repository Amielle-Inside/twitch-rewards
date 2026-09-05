from twitchrewards.models.trophies.early_user import EarlyUser
from twitchrewards.models.trophies.trophy import DbTrophy, Trophy


def specific_trophy(generic_trophy: DbTrophy) -> Trophy:
    if generic_trophy.id == 1:
        return EarlyUser(generic_trophy.redeemable)

    raise ValueError(f"Undefined trophy {generic_trophy}")
