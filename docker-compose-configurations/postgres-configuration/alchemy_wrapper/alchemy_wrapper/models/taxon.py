"""SQLalchemy model for taxon table."""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from alchemy_wrapper import Session
from enpkg_interfaces import Taxon as TaxonInterface
from enpkg_interfaces.from_identifier import IdentifierNotFound
from .base import Base


class Taxon(Base, TaxonInterface):
    """Define the Taxon model."""

    __tablename__ = "taxons"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    author_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, ondelete="CASCADE"
    )
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=DateTime.utcnow, onupdate=DateTime.utcnow
    )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Taxon({self.name!r})>"

    @staticmethod
    def from_id(identifier: int) -> "Taxon":
        """Return taxon instance from taxon id."""
        # We query the user table to get the user corresponding to the given identifier
        taxon = Taxon.query.filter_by(id=identifier).first()
        if taxon is None:
            raise IdentifierNotFound(f"Taxon with id {identifier} not found")
        return taxon

    def get_id(self) -> int:
        """Return taxon id."""
        return self.id

    def delete(self):
        """Delete the user."""
        # We delete the user from the database
        session = Session()
        session.delete(self)
        session.commit()
