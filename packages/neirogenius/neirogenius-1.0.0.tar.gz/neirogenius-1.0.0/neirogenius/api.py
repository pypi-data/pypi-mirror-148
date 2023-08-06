from requests import get
from .statistic import Statistic
from .errors import *
from .ping import Ping
from .attachments import Attachments
from .messages import Messages
from .settings import Settings


class API:
    """
    Neirogenius API wrapper.
    """

    BASE_URL = "https://neirogenius.herokuapp.com/"  # http://neirogenius.ru/ in future

    def __init__(self):
        pass

    def _get(self, endpoint) -> dict:
        """
        Get data from the api.

        Parameters
        ----------
        endpoint : str
            The endpoint to get data from.
        """
        url = f"{self.BASE_URL}{endpoint}"
        r = get(url)
        data = r.json()
        if 'error' in data:
            raise RateLimited()
        return data

    def get_statistic(self) -> Statistic:
        """
        Get statistic from the api.
        """
        return Statistic(self._get("statistic"))

    def get_ping(self) -> Ping:
        """
        Get ping from the api.
        """
        return Ping(self._get("ping"))

    def get_messages(self, guild_id: int) -> Messages:
        """
        Get messages from the api.

        Parameters
        ----------
        guild_id : int
            The guild id to get messages from.
        """
        return Messages(self._get(f"messages/{guild_id}"))

    def get_attachments(self, guild_id: int) -> Attachments:
        """
        Get attachments from the api.

        Parameters
        ----------
        guild_id : int
            The guild id to get attachments from.
        """
        return Attachments(self._get(f"attachments/{guild_id}"))

    def get_settings(self, guild_id: int) -> Settings:
        """
        Get settings from the api.

        Parameters
        ----------
        guild_id : int
            The guild id to get settings from.
        """
        return Settings(self._get(f"settings/{guild_id}"))
