class Ping:
    def __init__(self, data: dict):
        self.global_ping: int = data['global_ping']
        self.global_formatted_ping: str = data['global_formatted_ping']
        self.shards: list = data['shards']
