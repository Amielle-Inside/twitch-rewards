from dataclasses import dataclass

from twitchrewards.models.trophies.trophy import Trophy


@dataclass(init=False)
class EarlyUser(Trophy):
    id = 1
    name = "Chegou cedo"
    description = "Isso nem ta funcionando direito"
    image_path = "/static/img/trophies/early_user.png"
    redeemable: bool = False

    def __init__(self, redeemable):
        self.redeemable = redeemable
