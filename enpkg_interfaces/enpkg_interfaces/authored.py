"""Abstract interface describing the methods associated to an object with an author."""

from typing import Type
from enpkg_interfaces.user import User


class Authored(object):
    """Abstract interface describing the methods associated to an object with an author."""

    def get_author(self) -> Type[User]:
        """Return author user."""
        raise NotImplementedError(
            "Abstract method 'get_author' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
