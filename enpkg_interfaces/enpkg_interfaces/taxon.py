"""Abstract interface for taxon objects."""
from typing import List, Type
from enpkg_interfaces import Sample, Record


class Taxon(Record):
    """Abstract class to represent a taxon."""

    def get_samples(self) -> List[Type[Sample]]:
        """Return list of samples."""
        raise NotImplementedError(
            "Abstract method 'get_samples' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
