"""SQLAlchemy model for the samples table."""

from typing import List, Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from alchemy_wrapper import Session
from alchemy_wrapper.models import SpectraCollection
from enpkg_interfaces import Sample as SampleInterface
from enpkg_interfaces.from_identifier import IdentifierNotFound
from .base import Base
from .user import User


class Sample(Base, SampleInterface):
    id = Column(Integer, primary_key=True)
    taxon_id = Column(
        Integer, ForeignKey("taxons.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altitude = Column(Float, nullable=True)
    # The derived from column is a foreign key to the sample table
    # It is used to link a sample to the sample it was derived from
    # For example, if a sample is a subsample of another sample, the derived from column
    # will be set to the id of the sample it was derived from
    # If the sample is not derived from another sample, the derived from column will be
    # set to None
    # The ondelete="SET NULL" means that if the sample it was derived from is deleted,
    # the derived from column will be set to None
    # The nullable=True means that the derived from column can be set to None
    # If the derived from column is set to None, it means that the sample is not derived
    # from another sample
    derived_from = Column(
        Integer, ForeignKey("samples.id", ondelete="SET NULL"), nullable=True
    )

    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=DateTime.utcnow, onupdate=DateTime.utcnow
    )
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def get_parent_sample(self) -> Optional["Sample"]:
        """Return parent sample."""
        if self.derived_from is None:
            return None
        return Sample.from_id(self.derived_from)

    def get_child_samples(self) -> List["Sample"]:
        """Return list of child samples."""
        return Sample.query.filter_by(derived_from=self.id).all()

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

    def get_author(self) -> User:
        """Return the author of the sample."""
        return User.from_id(self.author_id)

    def delete(self):
        """Delete the sample."""
        # We delete the sample from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description

    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name

    def get_root(self) -> str:
        """Return recorded object root."""
        return "samples"

    def get_spectra_collections(self) -> List[SpectraCollection]:
        """Return list of spectra collections."""
        return SpectraCollection.query.filter_by(sample_id=self.id).all()
