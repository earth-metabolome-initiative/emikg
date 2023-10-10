"""SQLAlchemy models for spectra_collection table."""

from typing import List, Type
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from enpkg_interfaces import SpectraCollection as SpectraCollectionInterface
from enpkg_interfaces.from_identifier import IdentifierNotFound
from alchemy_wrapper.models import Base, Spectrum, User, Sample
from alchemy_wrapper import Session


class SpectraCollection(Base, SpectraCollectionInterface):
    """SQLAlchemy model for spectra_collection table."""

    __tablename__ = "spectra_collection"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    sample_id = Column(
        Integer, ForeignKey("samples.id", ondelete="CASCADE"), nullable=False
    )
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    updated_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=DateTime.utcnow)

    def get_spectra(self) -> List[Type[Spectrum]]:
        """Return a list of spectra."""
        raise NotImplementedError(
            "SpectraCollection.get_spectra() not implemented "
            f" for {self.__class__.__name__}"
        )

    def get_sample(self) -> Sample:
        """Return sample."""
        return Sample.from_id(self.sample_id)

    @staticmethod
    def from_id(identifier: int) -> "SpectraCollection":
        """Return SpectraCollection instance from SpectraCollection id."""
        # We query the user table to get the user corresponding to the given identifier
        spectra_collection = SpectraCollection.query.filter_by(id=identifier).first()
        if spectra_collection is None:
            raise IdentifierNotFound(
                f"SpectraCollection with id {identifier} not found"
            )
        return spectra_collection

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def delete(self):
        """Delete the spectra collection."""
        # We delete the spectra collection from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_author(self) -> User:
        """Return the author of the spectrum."""
        return User.from_id(self.author_id)

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description

    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name