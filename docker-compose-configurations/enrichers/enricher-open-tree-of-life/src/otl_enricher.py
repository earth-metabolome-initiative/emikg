"""Concrete implementation for the Open Tree of Life taxon Enricher."""
from enrichers import TaxonEnricher
from alchemy_wrapper.models import Taxon
from alchemy_wrapper import Session
from .models import OpenTreeOfLifeEntry


class OTLEnricher(TaxonEnricher):
    @classmethod
    def repository_name(cls) -> str:
        """Name of the repository providing these specific metadata."""
        return "Open Tree of Life"

    def _can_enrich(self, enrichable: Taxon) -> bool:
        """Returns whether the Enricher can enrich the metadata of the enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        if not isinstance(enrichable, Taxon):
            return False

        # A Taxon is enrichable if there is not already an entry in the
        # open_tree_of_life table with the same taxon_id.
        return (
            OpenTreeOfLifeEntry.query.filter_by(taxon_id=enrichable.id).first() is None
        )

    def _enrich(self, enrichable: Taxon):
        """Enrich the metadata of a enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        # We create a new entry in the open_tree_of_life table
        # with the taxon_id of the enrichable class.
        session = Session()
        entry = OpenTreeOfLifeEntry(ott_id=None, taxon_id=enrichable.id)
        session.add(entry)
        session.commit()
