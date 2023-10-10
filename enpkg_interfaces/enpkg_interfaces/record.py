"""Abstract interface for an object that has been recorded."""

from enpkg_interfaces.deletable import Deletable
from enpkg_interfaces.from_identifier import FromIdentifier


class Record(FromIdentifier, Deletable):
    """Abstract class to represent a recorded object."""

    def get_name(self) -> str:
        """Return recorded object name."""
        raise NotImplementedError(
            "Abstract method 'get_name' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_description(self) -> str:
        """Return recorded object description."""
        raise NotImplementedError(
            "Abstract method 'get_description' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
    
    def get_root(self) -> str:
        """Return recorded object root."""
        raise NotImplementedError(
            "Abstract method 'get_root' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_url(self) -> str:
        """Return recorded object URL."""
        return f"/{self.get_root()}/{self.get_id()}"