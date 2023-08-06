class Statistic:
    """
    This class represents statistic.

    Attributes
    ----------
    guilds_count : str
        The number of guilds to which the bot has been added.
    users_count : int
        Total bot users count.
    attachments_count : int or None
        Total attachments count.
    messages_count : int
        Total messages count.
    guilds : list[:class:`Guild`]
        List of :class:`Guild` instances, that bot was added to.
    """

    def __init__(self, data: dict) -> None:
        self.guilds_count: int = int(data["guilds_count"])
        self.users_count: int = int(data["users_count"])
        self.attachments_count: int = int(data["attachments_count"])
        self.messages_count: int = int(data["messages_count"])
        self.guilds: list[Guild] = list(map(Guild, data["guilds"]))


class Guild:
    """
    This class represents guild from statistic.

    Attributes
    ----------
    name : str
        Name of guild.
    members_count : int
        Count of members in this guild.
    """

    def __init__(self, data: dict) -> None:
        self.name: str = data["name"]
        self.members_count: int = int(data["members_count"])
