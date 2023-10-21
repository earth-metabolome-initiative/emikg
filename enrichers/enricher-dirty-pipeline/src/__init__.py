"""Package for the Dirty Pipeline Enricher."""
from alchemy_wrapper.models.base import Base
from alchemy_wrapper.database import engine
from .dirty_pipeline_enricher import DirtyPipelineEnricher

Base.metadata.create_all(bind=engine)

__all__ = ["DirtyPipelineEnricher"]