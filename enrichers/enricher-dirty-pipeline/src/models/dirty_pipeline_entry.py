"""SQLAlchemy database proxy relative to the dirty_pipeline_entries table"""
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql import func
from alchemy_wrapper.models.base import Base


class DirtyPipelineEntry(Base):
    """Define the DirtyPipelineEntry model."""

    __tablename__ = "dirty_pipeline_entries"

    id = Column(Integer, primary_key=True)
    payload_id = Column(Integer, ForeignKey("data_payloads.id"), nullable=False)

    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<DirtyPipelineEntry({self.ott_id!r})>"
