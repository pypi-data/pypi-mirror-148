class Messages:
    def __init__(self, data: dict):
        self.messages_count: int = data['messages_count']
        self.last_message_timestamp: int = data['last_message_timestamp']
        self.messages: list = data['messages']
