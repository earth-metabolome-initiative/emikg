"""Abstract interface for user objects."""
from typing import Type

from enpkg_interfaces.sample import Sample
from enpkg_interfaces.taxon import Taxon


class User:
    """Abstract class to represent a user."""

    def get_user_id(self) -> int:
        """Return user ID."""
        raise NotImplementedError(
            "Abstract method 'get_user_id' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

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

    def is_author_of_sample(self, sample: Type[Sample]) -> bool:
        """Return True if the user is the author of the sample."""
        return self.get_user_id() == sample.get_author_user_id()

    def is_author_of_taxon(self, taxon: Type[Taxon]) -> bool:
        """Return True if the user is the author of the taxon."""
        return self.get_user_id() == taxon.get_author_user_id()

    def delete(self):
        """Delete the user."""
        raise NotImplementedError(
            "Abstract method 'delete' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )
