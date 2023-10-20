"""Submodule providing table interfaces associated to the enrichers service."""
from .enricher import Enricher
from .taxon_enrichment_task import TaxonEnrichmentTask

__all__ = ["Enricher", "TaxonEnrichmentTask"]
