"""SQLAlchemy table for the tasks involving enrichemnt of taxons."""

from sqlalchemy import Column, Integer, ForeignKey
from .base import Base


class TaxonEnrichmentTask(Base):
    """Define the TaxonEnrichmentTask model."""

    __tablename__ = "taxon_enrichment_tasks"

    id = Column(Integer, primary_key=True)

    # We associate to the taxon id from the taxons table, which cascade upon deletion of the taxon
    # foreign key
    taxon_id = Column(
        Integer, ForeignKey("taxons.id"), nullable=False, ondelete="CASCADE"
    )
    task_id = Column(
        Integer, ForeignKey("enrichers_tasks.id"), ondelete="CASCADE", nullable=False
    )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TaxonEnrichmentTask({self.taxon_id!r})>"