"""Class for when the user request is unauthorized."""

from .api_exception import APIException

class Unauthorized(APIException):
    """Exception raised when a user request is unauthorized."""

    def __init__(self):
        """Initialize the exception."""
        super().__init__("You are not authorized to perform this action.")