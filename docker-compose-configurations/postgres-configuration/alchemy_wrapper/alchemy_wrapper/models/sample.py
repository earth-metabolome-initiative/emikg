"""SQLAlchemy model for the samples table."""

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from alchemy_wrapper import Session
from enpkg_interfaces import Sample as SampleInterface
from enpkg_interfaces.from_identifier import IdentifierNotFound
from .base import Base


class Sample(Base, SampleInterface):
    id = Column(Integer, primary_key=True)
    taxon_id = Column(
        Integer, ForeignKey("taxons.id", ondelete="CASCADE"), nullable=False
    )
    sample_name = Column(String(255), nullable=False)
    sample_description = Column(String(512), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altitude = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=DateTime.utcnow, onupdate=DateTime.utcnow
    )
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    @staticmethod
    def from_id(identifier: int) -> "Sample":
        """Return Sample instance from Sample id."""
        # We query the user table to get the user corresponding to the given identifier
        sample = Sample.query.filter_by(id=identifier).first()
        if sample is None:
            raise IdentifierNotFound(f"Sample with id {identifier} not found")
        return sample

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def delete(self):
        """Delete the user."""
        # We delete the user from the database
        session = Session()
        session.delete(self)
        session.commit()
