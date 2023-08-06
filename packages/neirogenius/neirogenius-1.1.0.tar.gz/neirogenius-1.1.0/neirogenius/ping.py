class Ping:
    """
    This class represents ping, that belongs to bot.

    Attributes
    ----------
    global_ping : int
        Global bot ping.
    global_formatted_ping : int
        Formatted version of `global_ping`.
    shards : list[:class:`Shard`]
        List of shards, that the bot have.
    """

    def __init__(self, data: dict) -> None:
        self.global_ping: int = int(data["global_ping"])
        self.global_formatted_ping: str = data["global_formatted_ping"]
        self.shards: list[Shard] = list(map(Shard, data["shards"]))


class Shard:
    """
    This class represents shard, that belongs to bot.

    Attributes
    ----------
    shard_ping : int
        Shard's ping.
    shard_formatted_ping : str
        Formatted version of `shard_ping`.
    """

    def __init__(self, data: dict) -> None:
        self.shard_ping: int = int(data["shard_ping"])
        self.shard_formatted_ping: str = data["shard_formatted_ping"]
