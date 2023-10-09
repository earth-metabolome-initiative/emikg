"""Abstract interface for user objects."""
from typing import Type

from enpkg_interfaces.from_identifier import FromIdentifier
from enpkg_interfaces.authored import Authored


class User(FromIdentifier):
    """Abstract class to represent a user."""

    def is_administrator(self) -> bool:
        """Return True if the user is an administrator."""
        raise NotImplementedError(
            "Abstract method 'is_administrator' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    def is_moderator(self) -> bool:
        """Return True if the user is a moderator."""
        raise NotImplementedError(
            "Abstract method 'is_moderator' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    def is_author_of(self, authored: Type[Authored]) -> bool:
        """Return True if the user is the author of the provided authored object."""
        return self.get_id() == authored.get_author().get_id()

    def delete(self):
        """Delete the user."""
        raise NotImplementedError(
            "Abstract method 'delete' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )
