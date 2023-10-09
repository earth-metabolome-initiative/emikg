"""Abstract interface for spectrum objects."""
from enpkg_interfaces.from_identifier import FromIdentifier
from enpkg_interfaces.authored import Authored
from enpkg_interfaces.deletable import Deletable


class Spectrum(FromIdentifier, Authored, Deletable):
    """Abstract class to represent a spectrum."""
