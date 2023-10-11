"""Abstract interface for spectrum objects."""
from emikg_interfaces.record import Record
from emikg_interfaces.spectra_collection import SpectraCollection
from emikg_interfaces.authored import Authored

class Spectrum(Record, Authored):
    """Abstract class to represent a spectrum."""

    def get_spectra_collection(self) -> SpectraCollection:
        """Return spectra collection."""
        raise NotImplementedError(
            "Abstract method 'get_spectra_collection' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    @staticmethod
    def get_root() -> str:
        """Return root for the spectrum interface."""
        return "spectra"