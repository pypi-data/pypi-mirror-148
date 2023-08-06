class Attachments:
    def __init__(self, data: dict):
        self.attachments_count = data['attachments_count']
        self.last_attachment_timestamp = data['last_attachment_timestamp']
        self.attachments: list = data['attachments']
