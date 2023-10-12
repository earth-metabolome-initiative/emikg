"""SQLAlchemy model for translation table for handling multi-language version of textual messages."""
from sqlalchemy import Column, Integer, String, DateTime
from alchemy_wrapper.models.base import Base

class Translation(Base):
    """Define the Translation model."""

    __tablename__ = "translation"

    id = Column(Integer, primary_key=True)
    language_code = Column(String(2), nullable=False)
    label = Column(String(255), nullable=False)
    translation = Column(String(512), nullable=False)
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=DateTime.utcnow, onupdate=DateTime.utcnow)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Translation({self.label!r})>"
    