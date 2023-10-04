"""SQLalchemy model for taxon table."""
from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base


class Taxon(Base):
    """Define the Taxon model."""

    __tablename__ = "taxons"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    author_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, ondelete="CASCADE"
    )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Taxon({self.name!r})>"