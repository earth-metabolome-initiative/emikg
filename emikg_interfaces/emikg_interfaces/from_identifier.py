"""Abstract interface providing the method from_id."""
from typing import Type


class FromIdentifier(object):
    """Abstract interface providing the method from_id."""

    def get_id(self) -> int:
        """Return the identifier of the object."""
        raise NotImplementedError(
            "Class does not implement method get_id. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    @staticmethod
    def from_id(identifier: int) -> Type["FromIdentifier"]:
        """Return the  object corresponding to the given identifier.

        Parameters
        ----------
        identifier : int
            The identifier of the object to return.

        Raises
        ------
        PackageNotFound
            If the package corresponding to the given identifier is not found.
        """
        raise NotImplementedError("Class does not implement method from_id")


# We also define a child exception class for the case where the object is not found
class IdentifierNotFound(Exception):
    """Exception raised when an object is not found."""
