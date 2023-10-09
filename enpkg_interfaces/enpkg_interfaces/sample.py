"""Abstract interface for sample objects."""
from typing import List, Type, Optional
from enpkg_interfaces.from_identifier import FromIdentifier
from enpkg_interfaces.authored import Authored
from enpkg_interfaces.deletable import Deletable

class Sample(FromIdentifier, Authored, Deletable):
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