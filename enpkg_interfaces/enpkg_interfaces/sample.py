"""Abstract interface for sample objects."""
from typing import List, Type

class Sample:
    """Abstract class to represent a sample."""

    def __init__(self, sample_id: int) -> None:
        """Initialize sample object.
        
        Parameters
        ----------
        sample_id : int
            sample ID.

        Raises
        ------
        ValueError
            If the sample ID does not exist.
        """
        if not Sample.is_valid_sample_id(sample_id):
            raise ValueError(
                f"Sample ID #{sample_id} does not exist."
            )
        
        self._sample_id = sample_id

    @staticmethod
    def is_valid_sample_id(sample_id: int) -> bool:
        """Check if sample ID exists.

        Parameters
        ----------
        sample_id : int
            sample ID.

        Returns
        -------
        bool
            True if sample ID exists, False otherwise.
        """
        raise NotImplementedError(
            "Abstract method 'is_valid_sample_id' should be implemented in derived class. "
        )
    
    @staticmethod
    def is_valid_sample_name(sample_name: str) -> bool:
        """Check if sample name exists.

        Parameters
        ----------
        sample_name : str
            sample name.

        Returns
        -------
        bool
            True if sample name exists, False otherwise.
        """
        raise NotImplementedError(
            "Abstract method 'is_valid_sample_name' should be implemented in derived class. "
        )

    def get_sample_id(self) -> int:
        """Return sample ID."""
        return self._sample_id

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
            f"#{self.get_sample_id()} is not derived from another sample."
        )
    
    def get_child_samples(self) -> List[Type["Sample"]]:
        """Return list of child samples."""
        raise NotImplementedError(
            "Abstract method 'get_child_samples' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
    
    def get_author_user_id(self) -> int:
        """Return author user ID."""
        raise NotImplementedError(
            "Abstract method 'get_author_user_id' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )