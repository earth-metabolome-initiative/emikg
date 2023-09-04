"""Abstract API exception class."""
from typing import Dict

class APIException(Exception):
    """Abstract API exception class."""

    def to_json(self) -> Dict[str, str]:
        """Return JSON representation of the exception."""
        return {
            "error": self.__class__.__name__,
            "message": str(self)
        }