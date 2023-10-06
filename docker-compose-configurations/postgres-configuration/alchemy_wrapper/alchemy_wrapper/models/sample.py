"""SQLAlchemy model for the samples table."""

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from .base import Base

class Sample(Base):
    id = Column(Integer, primary_key=True)
    taxon_id = Column(Integer, ForeignKey("taxons.id", ondelete="CASCADE"), nullable=False)
    sample_name = Column(String(255), nullable=False)
    sample_description = Column(String(512), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altitude = Column(Float, nullable=True)
    creation_date = Column(DateTime, nullable=False, default=DateTime.utcnow)
