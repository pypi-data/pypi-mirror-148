class APIException(Exception):
    """An error involving the Neirogenius api."""


class RateLimited(APIException):
    def __init__(self):
        super().__init__("Rate limited. Try again in a few seconds.")
