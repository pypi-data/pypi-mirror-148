from requests import get

from .attachments import Attachments
from .errors import *
from .messages import Messages
from .ping import Ping
from .settings import Settings
from .statistic import Statistic


class API:
    """
    Neirogenius API wrapper.

    Attributes
    ----------
    base_url : str
        Base URL where will the requests go

    Methods
    -------
    get_statistic()
        Get statistic from the API.
    get_ping()
         Get ping from the API.
    get_messages(guild_id: int)
        Get messages from the API.
    get_attachments(guild_id: int)
        Get attachments from the API.
    get_settings(guild_id: int)
        Get settings from the API.
    """

    def __init__(self) -> None:
        self.base_url: str = "https://api.neirogenius.ru/"

    def __fetch(self, endpoint: str) -> dict:
        """
        Fetch data from the API.

        Parameters
        ----------
        endpoint : str
            The endpoint to get data from.

        Returns
        -------
        dict
            Fetched data from API.
        """
        request = get(f"{self.base_url}{endpoint}")
        data = request.json()
        if request.status_code == 429:
            raise RateLimited()
        return data

    def get_statistic(self) -> Statistic:
        """
        Get statistic from the API.

        Returns
        -------
        :class:`Statistic`
            Fetched and parsed class.
        """
        return Statistic(self.__fetch("statistic"))

    def get_ping(self) -> Ping:
        """
        Get ping from the API.

        Returns
        -------
        :class:`Ping`
            Fetched and parsed class.
        """
        return Ping(self.__fetch("ping"))

    def get_messages(self, guild_id: int) -> Messages:
        """
        Get messages from the API.

        Parameters
        ----------
        guild_id : int
            The guild ID to get messages from.

        Returns
        -------
        :class:`Messages`
            Fetched and parsed class.
        """
        return Messages(self.__fetch(f"messages/{guild_id}"))

    def get_attachments(self, guild_id: int) -> Attachments:
        """
        Get attachments from the API.

        Parameters
        ----------
        guild_id : int
            The guild ID to get attachments from.

        Returns
        -------
        :class:`Attachments`
            Fetched and parsed class.
        """
        return Attachments(self.__fetch(f"attachments/{guild_id}"))

    def get_settings(self, guild_id: int) -> Settings:
        """
        Get settings from the API.

        Parameters
        ----------
        guild_id : int
            The guild ID to get settings from.

        Returns
        -------
        :class:`Settings`
            Fetched and parsed class.
        """
        return Settings(self.__fetch(f"settings/{guild_id}"))
