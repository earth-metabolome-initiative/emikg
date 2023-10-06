"""Module for the NotLoggedIn exception."""
from .api_exception import APIException

class NotLoggedIn(APIException):
    """Exception raised when a user is not logged in."""

    def __init__(self):
        """Initialize the exception."""
        super().__init__("You are not logged in.")