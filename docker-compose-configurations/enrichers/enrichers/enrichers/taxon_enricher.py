"""Abstract Enricher class for extending the metadata of a taxon class."""

from typing import Type
from .enricher import Enricher
from .models import TaxonEnrichmentTask, EnrichmentTask
from .enrichable import Enrichable


class TaxonEnricher(Enricher):
    """Abstract Enricher class for extending the metadata of a taxon class."""

    def _create_new_task(self, enrichable: Type[Enrichable]) -> EnrichmentTask:
        enrichment_task = super()._create_new_task(enrichable)
        # Create a new entry in the taxon_enrichment_tasks table
        _taxon_enrichment_task = TaxonEnrichmentTask(
            taxon_id=enrichable.id, enrichment_task_id=enrichment_task.id
        )
        return enrichment_task
