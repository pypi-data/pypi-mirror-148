class APIException(Exception):
    """
    This class represents exception, that can be thrown while working with API.
    """

    ...


class RateLimited(APIException):
    """
    This class represents exception, that can be thrown when you're rate limited.
    """

    def __init__(self) -> None:
        super().__init__("You're rate limited. Try again in a few seconds.")
