"""Abstract interface for taxon objects."""

class Taxon:
    """Abstract class to represent a taxon."""

    def __init__(self, taxon_id: int) -> None:
        """Initialize taxon object.
        
        Parameters
        ----------
        taxon_id : int
            taxon ID.

        Raises
        ------
        ValueError
            If the taxon ID does not exist.
        """
        if not self.is_valid_taxon_id(taxon_id):
            raise ValueError(
                f"Taxon ID #{taxon_id} does not exist."
            )
        
        self._taxon_id = taxon_id

    @staticmethod
    def is_valid_taxon_id(taxon_id: int) -> bool:
        """Check if taxon ID exists.

        Parameters
        ----------
        taxon_id : int
            taxon ID.

        Returns
        -------
        bool
            True if taxon ID exists, False otherwise.
        """
        raise NotImplementedError(
            "The method is_valid_taxon_id() must be implemented "
            "in the child classes of Taxon. "
        )
    
    @staticmethod
    def is_valid_taxon_name(taxon_name: str) -> bool:
        """Check if taxon name exists.

        Parameters
        ----------
        taxon_name : str
            taxon name.

        Returns
        -------
        bool
            True if taxon name exists, False otherwise.
        """
        raise NotImplementedError(
            "The method is_valid_taxon_name() must be implemented "
            "in the child classes of Taxon. "
        )
    
    def get_author_user_id(self) -> int:
        """Return author user ID."""
        raise NotImplementedError(
            "Abstract method 'get_author_user_id' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
    
    def get_taxon_name(self) -> str:
        """Return taxon name."""
        raise NotImplementedError(
            "Abstract method 'get_taxon_name' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
    
    def get_taxon_id(self) -> int:
        """Return taxon ID."""
        raise NotImplementedError(
            "Abstract method 'get_taxon_id' should be implemented in derived class. "
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