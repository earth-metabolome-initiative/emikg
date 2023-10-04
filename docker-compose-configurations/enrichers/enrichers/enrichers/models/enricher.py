"""Submodule providing enrichers models."""
from sqlalchemy import Column, Integer, String
from .base import Base


class Enricher(Base):
    """Define the Enricher model."""

    __tablename__ = "enrichers"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Enricher({self.name!r})>"
