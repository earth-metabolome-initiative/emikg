"""Module providing custom exceptions for the API."""

from .not_logged_in import NotLoggedIn
from .api_exception import APIException
from .unauthorized import Unauthorized

__all__ = ["NotLoggedIn", "Unauthorized", "APIException"]