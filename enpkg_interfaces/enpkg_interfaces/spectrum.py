"""Abstract interface for spectrum objects."""
from enpkg_interfaces.from_identifier import FromIdentifier
from enpkg_interfaces.authored import Authored


class Spectrum(FromIdentifier, Authored):
    """Abstract class to represent a spectrum."""
