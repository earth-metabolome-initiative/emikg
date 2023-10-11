"""Package providing interfaces used across the emikg project."""
from emikg_interfaces.sample import Sample
from emikg_interfaces.taxon import Taxon
from emikg_interfaces.user import User
from emikg_interfaces.spectrum import Spectrum
from emikg_interfaces.record import Record
from emikg_interfaces.spectra_collection import SpectraCollection
from emikg_interfaces.from_identifier import FromIdentifier, IdentifierNotFound

__all__ = [
    "Sample",
    "Taxon",
    "User",
    "Spectrum",
    "Record",
    "SpectraCollection",
    "FromIdentifier",
    "IdentifierNotFound"
]