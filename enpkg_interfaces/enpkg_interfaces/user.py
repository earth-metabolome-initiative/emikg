"""Abstract interface for user objects."""
from typing import Type

from enpkg_interfaces import Record
from enpkg_interfaces.authored import Authored


class User(Record):
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

    def get_taxons(self):
        """Return list of taxons created by the user."""
        raise NotImplementedError(
            "Abstract method 'get_taxons' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    def get_samples(self):
        """Return list of samples created by the user."""
        raise NotImplementedError(
            "Abstract method 'get_samples' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    def get_spectra(self):
        """Return list of spectra created by the user."""
        raise NotImplementedError(
            "Abstract method 'get_spectra' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )
    