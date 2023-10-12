from alchemy_wrapper.models.base import Base
from alchemy_wrapper.database import engine
from .taxon_enricher import TaxonEnricher
from .enricher import Enricher

Base.metadata.create_all(bind=engine)

__all__ = ["Enricher", "TaxonEnricher"]
