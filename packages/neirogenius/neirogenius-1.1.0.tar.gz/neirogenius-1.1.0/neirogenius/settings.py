from typing import Union


class Settings:
    """
    This class represents guild's settings.

    Attributes
    ----------
    id : str
        Unique guild ID that stored in database.
    guild_id : int
        Discord's guild ID.
    messages_channel : int or None
        Channel, that bot will respond in.
    random_chance : int
        Chance of random respond from bot.
    random_enabled : bool
        Will bot respond with random or not.
    format_messages : bool
        Will bot format messages in his response.
    """

    def __init__(self, data: dict) -> None:
        self.id: str = data["id"]
        self.guild_id: int = int(data["guide_id"])
        self.messages_channel: Union[int, None] = data["messages_channel_id"]
        if self.messages_channel is not None:
            self.messages_channel = int(self.messages_channel)
        self.random_chance: int = int(data["random_chance"])
        self.random_enabled: bool = bool(data["random_enabled"])
        self.format_messages: bool = bool(data["format_messages"])
