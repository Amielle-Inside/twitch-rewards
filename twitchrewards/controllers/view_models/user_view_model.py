"""User representation returned by the API"""

from dataclasses import dataclass
from typing import List

from twitchrewards.models import Trophy


@dataclass
class UserViewModel:
    """This should be moved to return a plain user, and pronouns should be parsed on view"""

    display_name: str
    pronouns: str
    pronouns_id: int
    trophies: List[Trophy]
