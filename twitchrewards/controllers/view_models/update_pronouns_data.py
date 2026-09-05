"""Request body for the update pronouns endpoint"""

from dataclasses import dataclass

from twitchrewards.models import Pronouns


@dataclass
class UpdatePronounsData:
    """Wraps the data required for updating the pronouns of a user"""

    pronouns: Pronouns
