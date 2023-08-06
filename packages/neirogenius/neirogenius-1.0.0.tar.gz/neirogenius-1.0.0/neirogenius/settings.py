from typing import Union


class Settings:
    def __init__(self, data: dict):
        self.guide_id: int = data['guide_id']
        self.messages_channel: int = Union[data['messages_channel_id'], None]
        self.random_chance: int = data['random_chance']
        self.random_enabled: bool = data['random_enabled']
        self.format_messages: bool = data['format_messages']
        self.id: str = data['id']
