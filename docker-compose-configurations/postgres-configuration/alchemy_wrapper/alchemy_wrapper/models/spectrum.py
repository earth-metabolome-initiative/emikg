"""SQLAlchemy model for the spectrographic data."""
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from .base import Base


class Spectrum(Base):
    id = Column(Integer, primary_key=True)
    sample_id = Column(
        Integer, ForeignKey("samples.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=DateTime.utcnow, onupdate=DateTime.utcnow
    )
    author_id  = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    