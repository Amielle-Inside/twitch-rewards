"""Returns the actual display name for the user given their title"""

from abc import ABC, abstractmethod

from twitchrewards.models import Pronouns, Title


def get_name_with_title(title: Title, display_name: str, pronouns: Pronouns):
    """
    Returns the name to show in chat.

    Parameters:
        title (Title): Regular display name of the user.
        display_name(str): Current twitch display name.
        pronouns(Pronouns): User's pronouns.

    Returns:
        str: The name to show in chat.
    """
    if not title in _title_lookup:
        return display_name

    title_description = _title_lookup[title]
    if pronouns == Pronouns.HE:
        return title_description.get_he(display_name)
    if pronouns == Pronouns.SHE:
        return title_description.get_she(display_name)
    if pronouns == Pronouns.THEY:
        return title_description.get_they(display_name)

    return title_description.get_she(display_name)


class TitleDescription(ABC):
    """Base class to ensure titles implement a description for available pronouns"""

    @abstractmethod
    def get_he(self, display_name: str):
        """
        Return display name for a user using 'he/him' pronouns.

        Parameters:
            display_name (str): Regular display name of the user.

        Returns:
            str: Actual name to display, considering the user's title.
        """

    @abstractmethod
    def get_she(self, display_name: str):
        """
        Return display name for a user using 'she/her' pronouns.

        Parameters:
            display_name (str): Regular display name of the user.

        Returns:
            str: Actual name to display, considering the user's title.
        """

    @abstractmethod
    def get_they(self, display_name: str):
        """
        Return display name for a user using 'they/them' pronouns.

        Parameters:
            display_name (str): Regular display name of the user.

        Returns:
            str: Actual name to display, considering the user's title.
        """


class Streamer(TitleDescription):
    """Streamer user title"""

    @staticmethod
    def to_string(display_name: str):
        """
        Return display name for the Streamer title.

        Parameters:
            display_name (str): Regular display name of the user.

        Returns:
            str: Name to show in chat, considering the user's title.
        """
        return f"Streamer {display_name}"

    def get_he(self, display_name: str):
        return self.to_string(display_name)

    def get_she(self, display_name: str):
        return self.to_string(display_name)

    def get_they(self, display_name: str):
        return self.to_string(display_name)


_title_lookup = {Title.STREAMER: Streamer()}
