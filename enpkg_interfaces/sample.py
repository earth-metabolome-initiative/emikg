"""Abstract interface for sample objects."""

class Sample:
    """Abstract class to represent a sample."""

    def is_derived_sample(self) -> bool:
        """Return True if sample is derived from another sample."""
        raise NotImplementedError(
            "Abstract method 'is_derived_sample' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
    
    def get_parent_sample(self) -> "Sample":
        """Return parent sample."""
        raise NotImplementedError(
            "Abstract method 'get_parent_sample' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )