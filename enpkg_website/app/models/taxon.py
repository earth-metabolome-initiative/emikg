"""Concretely implements the proxy taxon interface using SQLAlchemy."""
from enpkg_interfaces import Taxon as TaxonInterface

from ..app import db

class Taxon(TaxonInterface):
    """Class to represent a taxon."""

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

        Implementative details
        ----------------------
        The method looks up whether the taxon ID exists in taxon_id
        column of the taxons table.
        """
        return db.session.query(
            db.exists().where(
                db.and_(
                    db.table("taxons").column("taxon_id") == taxon_id
                )
            )
        ).scalar()