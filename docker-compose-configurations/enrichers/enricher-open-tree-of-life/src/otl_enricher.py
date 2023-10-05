"""Concrete implementation for the Open Tree of Life taxon Enricher."""
from typing import List
from enrichers import TaxonEnricher
from enrichers.models import EnrichmentTask
from alchemy_wrapper.models import Taxon
from alchemy_wrapper import Session
from .models import OpenTreeOfLifeEntry


class OTLEnricher(TaxonEnricher):
    @classmethod
    def repository(cls) -> str:
        """Name of the repository providing these specific metadata."""
        return "Open Tree of Life"

    @classmethod
    def name(cls) -> str:
        """Name of the enricher."""
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

    def _get_sleep_time_between_start_attempts(self) -> int:
        """Returns the number of seconds to wait between two start attempts."""
        return 10

    def _task_can_start(self, enrichable: Taxon) -> bool:
        """Returns whether the task can start.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        # A task can start if there is not already an entry in the
        # open_tree_of_life table with the same taxon_id.
        return self._can_enrich(enrichable)

    def _get_new_elements_to_enrich(self) -> List[Taxon]:
        """Returns a list of new elements to enrich."""
        # Get all the taxons that are not already in the open_tree_of_life table.
        return Taxon.query.filter(
            ~Taxon.id.in_(
                self._session.query(OpenTreeOfLifeEntry.taxon_id).filter(
                    OpenTreeOfLifeEntry.taxon_id.isnot(None)
                )
            )
        ).all()

    def _enrich(self, enrichable: Taxon, task: EnrichmentTask):
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
