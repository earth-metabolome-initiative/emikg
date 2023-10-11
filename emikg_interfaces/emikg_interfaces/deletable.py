"""Abstract class for deletable objects."""


class Deletable:
    """Abstract class for deletable objects."""

    def delete(self):
        """Delete the object."""
        raise NotImplementedError(
            "Abstract method 'delete' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )
