"""Concrete implementation for the Dirty Pipeline enricher.

Implementative details
----------------------
The dirty pipeline enricher is an enricher based on the original dirty pipeline
built as a sequence of python repositories. This enricher is meant to be a temporary
solution to provide the complete enrichment for a given user provided payload, but
it really isn't meant to be a long term solution.

We want a precise clockwork swiss army knife for the enrichment, and the dirty pipeline
is more like a pipebomb. 
"""
from typing import List

from alchemy_wrapper.models import DataPayload, Task
from enrichers import Enricher

from .models import DirtyPipelineEntry


class DirtyPipelineEnricher(Enricher):
    """Concrete implementation for the Dirty Pipeline enricher."""

    @classmethod
    def repository(cls) -> str:
        """Name of the repository providing these specific metadata."""
        return "Dirty Pipeline"

    @classmethod
    def name(cls) -> str:
        """Name of the enricher."""
        return "Dirty Pipeline"

    def _can_enrich(self, enrichable: DataPayload) -> bool:
        """Returns whether the Enricher can enrich the metadata of the enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        if not isinstance(enrichable, DataPayload):
            return False
        
        return (
            self._session.query(DirtyPipelineEntry).filter_by(payload_id=enrichable.get_id()).first() is None
        )

    def _get_sleep_time_between_start_attempts(self) -> int:
        """Returns the number of seconds to wait between two start attempts."""
        return 10

    def _task_can_start(self, enrichable: DataPayload, task: Task) -> bool:
        """Returns whether the task can start.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        # A task can start if there is not already an entry in the
        # open_tree_of_life table with the same DataPayload_id.
        return self._can_enrich(enrichable)

    def _get_new_elements_to_enrich(self) -> List[DataPayload]:
        """Returns a list of new elements to enrich."""
        # Get all the DataPayloads that are not already in the dirty_pipeline_entries table.
        return self._session.query(DataPayload).filter(
            ~DataPayload.id.in_(
                self._session.query(DirtyPipelineEntry.payload_id)
            )
        ).all()

    def _enrich(self, enrichable: DataPayload, task: Task):
        """Enrich the metadata of a enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        raise NotImplementedError("This method should be implemented in derived classes.")

