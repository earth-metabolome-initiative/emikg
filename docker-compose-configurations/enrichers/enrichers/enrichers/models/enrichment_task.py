"""Submodule providing the Enrichments task SQLAlchemy model."""
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from .base import Base


class EnrichmentTask(Base):
    """Define the EnrichmentTask model."""

    __tablename__ = "enrichment_tasks"

    id = Column(Integer, primary_key=True)
    enricher_id = Column(
        Integer, ForeignKey("enrichers.id"), nullable=False, ondelete="CASCADE"
    )
    status = Column(
        Enum("PENDING", "STARTED", "SUCCESS", "FAILURE", name="status"),
        nullable=False,
        default="PENDING",
    )
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=DateTime.utcnow, onupdate=DateTime.utcnow)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<EnrichmentTask({self.id!r})>"

    def start(self):
        """Start the task."""
        self.status = "STARTED"

    def success(self):
        """Finish the task successfully."""
        self.status = "SUCCESS"

    def failure(self):
        """Finish the task with a failure."""
        self.status = "FAILURE"