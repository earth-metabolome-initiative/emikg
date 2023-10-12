from alchemy_wrapper.models.base import Base
from alchemy_wrapper.database import engine
from .otl_enricher import OTLEnricher

Base.metadata.create_all(bind=engine)

__all__ = ["OTLEnricher"]