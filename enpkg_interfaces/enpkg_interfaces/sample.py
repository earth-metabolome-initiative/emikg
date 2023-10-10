"""Abstract interface for sample objects."""
from typing import List, Optional, Type

from enpkg_interfaces.record import Record
from enpkg_interfaces.authored import Authored


class Sample(Record, Authored):
    """Abstract class to represent a sample."""

    def is_derived_sample(self) -> bool:
        """Return True if sample is derived from another sample."""
        return self.get_parent_sample() is not None

    def is_primary_sample(self) -> bool:
        """Return True if sample is primary sample, i.e. not derived from another sample."""
        return not self.is_derived_sample()

    def get_parent_sample(self) -> Optional[Type["Sample"]]:
        """Return parent sample."""
        raise NotImplementedError(
            "Abstract method '_get_parent_sample' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_child_samples(self) -> List[Type["Sample"]]:
        """Return list of child samples."""
        raise NotImplementedError(
            "Abstract method 'get_child_samples' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_spectra_collections(self) -> List[Type["SpectraCollection"]]:
        """Return list of spectra collections."""
        raise NotImplementedError(
            "Abstract method 'get_spectra_collections' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    @staticmethod
    def get_root() -> str:
        """Return root for the sample interface."""
        return "samples"