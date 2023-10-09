"""Abstract interface for taxon objects."""
from enpkg_interfaces.from_identifier import FromIdentifier
from enpkg_interfaces.authored import Authored
from enpkg_interfaces.deletable import Deletable

class Taxon(FromIdentifier, Authored, Deletable):
    """Abstract class to represent a taxon."""

    def get_taxon_name(self) -> str:
        """Return taxon name."""
        raise NotImplementedError(
            "Abstract method 'get_taxon_name' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_taxon_description(self) -> str:
        """Return taxon description."""
        raise NotImplementedError(
            "Abstract method 'get_taxon_description' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_taxon_url(self) -> str:
        """Return taxon URL."""
        raise NotImplementedError(
            "Abstract method 'get_taxon_url' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
