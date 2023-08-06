class Attachments:
    """
    This class represents list of attachments, that belongs to specific guild.

    Attributes
    ----------
    attachments_count : int
        Total count of guild's stored attachments.
    last_attachment_timestamp : int
        UNIX-point when the bot received last attachment.
    attachments : list[:class:`Attachment`]
        List of attachments, that this guild have.
    """

    def __init__(self, data: dict) -> None:
        self.attachments_count: int = int(data["attachments_count"])
        self.last_attachment_timestamp: int = int(data["last_attachment_timestamp"])
        self.attachments: list[Attachment] = list(map(Attachment, data["attachments"]))


class Attachment:
    """
    This class represents attachment, that stored in database.

    Attributes
    ----------
    id : str
        Unique ID for this attachment.
    url : str
        Attachment's content.
    guild_id : int
        ID of guild where this attachment was sent.
    timestamp : int
        UNIX-point when the bot received the attachment.
    message_id : int
        ID of attachment, that this object belongs to.
    author_id : int
        ID of sender of this attachment.
    """

    def __init__(self, data: dict) -> None:
        self.id: str = data.get("id")
        self.url: str = data.get("url")
        self.guild_id: int = int(data.get("guild_id"))
        self.timestamp: int = int(data.get("timestamp"))
        self.message_id: int = int(data.get("message_id"))
        self.author_id: int = int(data.get("author_id"))
