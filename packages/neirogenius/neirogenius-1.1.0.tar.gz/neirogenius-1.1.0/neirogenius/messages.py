class Messages:
    """
    This class represents list of messages, that belongs to specific guild.

    Attributes
    ----------
    messages_count : int
        Total count of guild's stored messages.
    last_message_timestamp : int
        UNIX-point when the bot received last message.
    messages : list[:class:`Message`]
        List of messages, that this guild have.
    """

    def __init__(self, data: dict) -> None:
        self.messages_count: int = int(data["messages_count"])
        self.last_message_timestamp: int = int(data["last_message_timestamp"])
        self.messages: list[Message] = list(map(Message, data["messages"]))


class Message:
    """
    This class represents message, that stored in database.

    Attributes
    ----------
    id : str
        Unique ID for this message.
    content : str
        Message's content.
    guild_id : int
        ID of guild where this message was sent.
    timestamp : int
        UNIX-point when the bot received the message.
    message_id : int
        ID of message, that this object belongs to.
    author_id : int
        ID of sender of this message.
    """

    def __init__(self, data: dict) -> None:
        self.id: str = data.get("id")
        self.content: str = data.get("content")
        self.guild_id: int = int(data.get("guild_id"))
        self.timestamp: int = int(data.get("timestamp"))
        self.message_id: int = int(data.get("message_id"))
        self.author_id: int = int(data.get("author_id"))
