"""Abstract interface for sample objects."""
from typing import List, Type
from enpkg_interfaces.from_identifier import FromIdentifier
from enpkg_interfaces.authored import Authored

class Sample(FromIdentifier, Authored):
    """Abstract class to represent a sample."""

    def is_derived_sample(self) -> bool:
        """Return True if sample is derived from another sample."""
        raise NotImplementedError(
            "Abstract method 'is_derived_sample' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def is_primary_sample(self) -> bool:
        """Return True if sample is primary sample, i.e. not derived from another sample."""
        return not self.is_derived_sample()

    def _get_parent_sample(self) -> Type["Sample"]:
        """Return parent sample."""
        raise NotImplementedError(
            "Abstract method '_get_parent_sample' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_parent_sample(self) -> Type["Sample"]:
        """Return parent sample."""
        if self.is_derived_sample():
            return self._get_parent_sample()

        raise ValueError(
            "It is not possible to return the parent sample because "
            f"#{self.get_id()} is not derived from another sample."
        )

    def get_child_samples(self) -> List[Type["Sample"]]:
        """Return list of child samples."""
        raise NotImplementedError(
            "Abstract method 'get_child_samples' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )