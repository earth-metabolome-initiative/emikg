"""Abstract interface for spectrum objects."""
from enpkg_interfaces import Record, SpectraCollection

class Spectrum(Record):
    """Abstract class to represent a spectrum."""

    def get_spectra_collection(self) -> SpectraCollection:
        """Return spectra collection."""
        raise NotImplementedError(
            "Abstract method 'get_spectra_collection' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )