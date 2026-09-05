"""Exposes members exported by the module"""

from twitchrewards.repository.trophy import get_by_id as get_trophy_by_id
from twitchrewards.repository.trophy import set_redeemable as set_trophy_redeemable
from twitchrewards.repository.user import add_trophy, create_user
from twitchrewards.repository.user import get_by_name as get_user_by_name
from twitchrewards.repository.user import update_active_trophies
from twitchrewards.repository.user import (
    update_profile_image_url as update_user_profile_image_url,
)
from twitchrewards.repository.user import update_user
