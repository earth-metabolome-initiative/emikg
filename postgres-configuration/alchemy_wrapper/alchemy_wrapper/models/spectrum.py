"""SQLAlchemy model for the spectrographic data."""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from alchemy_wrapper import Session
from alchemy_wrapper.models import SpectraCollection
from emikg_interfaces import Spectrum as SpectrumInterface
from emikg_interfaces.from_identifier import IdentifierNotFound
from alchemy_wrapper.models.base import Base
from alchemy_wrapper.models.user import User


class Spectrum(Base, SpectrumInterface):
    """SQLAlchemy model for the spectrographic data."""

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=False)
    spectra_collection_id = Column(
        Integer, ForeignKey("spectra_collection.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=DateTime.utcnow, onupdate=DateTime.utcnow
    )

    @staticmethod
    def from_id(identifier: int) -> "Spectrum":
        """Return Spectrum instance from Spectrum id."""
        # We query the user table to get the user corresponding to the given identifier
        spectrum = Spectrum.query.filter_by(id=identifier).first()
        if spectrum is None:
            raise IdentifierNotFound(f"Spectrum with id {identifier} not found")
        return spectrum

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def get_spectra_collection(self) -> SpectraCollection:
        """Return the spectra collection of the spectrum."""
        return SpectraCollection.from_id(self.spectra_collection_id)

    def get_author(self) -> User:
        """Return the author of the spectrum."""
        return self.get_spectra_collection().get_author()

    def delete(self):
        """Delete the spectrum."""
        # We delete the spectrum from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description

    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name