class Statistic:
    def __init__(self, data: dict):
        self.guilds_count: int = data['guilds_count']
        self.users_count: int = data['users_count']
        self.attachments_count: int = data['attachments_count']
        self.messages_count: int = data['messages_count']
        self.guilds: list = data['guilds']