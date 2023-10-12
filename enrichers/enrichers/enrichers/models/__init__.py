"""Submodule providing table interfaces associated to the enrichers service."""
from .enricher import Enricher
from .enrichment_task import EnrichmentTask
from .taxon_enrichment_task import TaxonEnrichmentTask

__all__ = ["Enricher", "EnrichmentTask", "TaxonEnrichmentTask"]
