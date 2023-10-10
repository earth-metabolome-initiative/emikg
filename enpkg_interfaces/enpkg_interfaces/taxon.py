"""Abstract interface for taxon objects."""
from typing import List, Type
from enpkg_interfaces.sample import Sample
from enpkg_interfaces.record import Record
from enpkg_interfaces.authored import Authored


class Taxon(Record, Authored):
    """Abstract class to represent a taxon."""

    def get_samples(self, number_of_records: int) -> List[Type[Sample]]:
        """Return list of samples.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        raise NotImplementedError(
            "Abstract method 'get_samples' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    @staticmethod
    def get_root() -> str:
        """Return root for the taxon interface."""
        return "taxons"