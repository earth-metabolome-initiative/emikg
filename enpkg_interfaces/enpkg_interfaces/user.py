"""Abstract interface for user objects."""
from typing import Type, List

from enpkg_interfaces import Record, SpectraCollection, Sample, Taxon
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

    def get_taxons(self, number_of_records: int) -> List[Type[Taxon]]:
        """Return list of taxons created by the user.
        
        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        raise NotImplementedError(
            "Abstract method 'get_taxons' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    def get_samples(self, number_of_records: int) -> List[Type[Sample]]:
        """Return list of samples created by the user.
        
        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        raise NotImplementedError(
            "Abstract method 'get_samples' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    def get_spectra_collections(self, number_of_records: int) -> List[Type[SpectraCollection]]:
        """Return list of spectra collections created by the user.
        
        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        raise NotImplementedError(
            "Abstract method 'get_spectra_collections' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )
