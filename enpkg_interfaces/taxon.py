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

    def is_valid_taxon_id(self, taxon_id: int) -> bool:
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
            f"It was not implemented in {self.__class__.__name__}."
        )