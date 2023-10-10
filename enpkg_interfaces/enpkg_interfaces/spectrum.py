"""Abstract interface for spectrum objects."""
from enpkg_interfaces.record import Record
from enpkg_interfaces.spectra_collection import SpectraCollection
from enpkg_interfaces.authored import Authored

class Spectrum(Record, Authored):
    """Abstract class to represent a spectrum."""

    def get_spectra_collection(self) -> SpectraCollection:
        """Return spectra collection."""
        raise NotImplementedError(
            "Abstract method 'get_spectra_collection' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )