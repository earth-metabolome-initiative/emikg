"""Abstract Enricher class for extending the metadata of a taxon class."""

from alchemy_wrapper.models import Taxon
from .enricher import Enricher
from .models import TaxonEnrichmentTask, EnrichmentTask


class TaxonEnricher(Enricher):
    """Abstract Enricher class for extending the metadata of a taxon class."""

    def _create_new_task(self, enrichable: Taxon) -> EnrichmentTask:
        enrichment_task = super()._create_new_task(enrichable)
        # Create a new entry in the taxon_enrichment_tasks table
        taxon_enrichment_task = TaxonEnrichmentTask(
            taxon_id=enrichable.id, enrichment_task_id=enrichment_task.id
        )
        self._session.add(taxon_enrichment_task)
        self._session.commit()
        return enrichment_task
