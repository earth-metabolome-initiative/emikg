"""SQLAlchemy table for the tasks involving enrichemnt of taxons."""

from sqlalchemy import Column, Integer, ForeignKey
from alchemy_wrapper.models.base import Base


class TaxonEnrichmentTask(Base):
    """Define the TaxonEnrichmentTask model."""

    __tablename__ = "taxon_enrichment_tasks"

    id = Column(Integer, primary_key=True)

    # We associate to the taxon id from the taxons table, which cascade upon deletion of the taxon
    # foreign key
    taxon_id = Column(
        Integer, ForeignKey("taxons.id", ondelete="CASCADE"), nullable=False, 
    )
    task_id = Column(
        Integer, ForeignKey("enrichment_tasks.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TaxonEnrichmentTask({self.taxon_id!r})>"