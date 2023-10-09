"""SQLalchemy model for taxon table."""
from typing import List

from alchemy_wrapper import Session
from alchemy_wrapper.models import Base, Sample, User
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from enpkg_interfaces import Taxon as TaxonInterface
from enpkg_interfaces.from_identifier import IdentifierNotFound


class Taxon(Base, TaxonInterface):
    """Define the Taxon model."""

    __tablename__ = "taxons"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(255), nullable=False)
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

    def get_samples(self) -> List[Sample]:
        """Return list of samples."""
        return Sample.query.filter_by(taxon_id=self.id).all()

    def get_author(self) -> User:
        """Return author."""
        return User.query.filter_by(id=self.author_id).first()
    
    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description
    
    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name
    
    def get_root(self) -> str:
        """Return recorded object root."""
        return "taxons"