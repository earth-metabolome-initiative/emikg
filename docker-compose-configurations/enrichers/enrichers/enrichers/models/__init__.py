"""Submodule providing table interfaces associated to the enrichers service."""
from alchemy_wrapper import engine
from .base import Base
from .enricher import Enricher
from .enrichment_task import EnrichmentTask
from .taxon_enrichment_task import TaxonEnrichmentTask

Base.metadata.create_all(bind=engine)

__all__ = ["Enricher", "EnrichmentTask", "TaxonEnrichmentTask"]
