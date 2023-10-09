"""SQLAlchemy model for the spectrographic data."""
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from alchemy_wrapper import Session
from enpkg_interfaces import Spectrum as SpectrumInterface
from enpkg_interfaces.from_identifier import IdentifierNotFound
from .base import Base


class Spectrum(Base, SpectrumInterface):
    id = Column(Integer, primary_key=True)
    sample_id = Column(
        Integer, ForeignKey("samples.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=DateTime.utcnow, onupdate=DateTime.utcnow
    )
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
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

    def delete(self):
        """Delete the user."""
        # We delete the user from the database
        session = Session()
        session.delete(self)
        session.commit()
