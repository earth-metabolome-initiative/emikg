"""Package providing interfaces used across the emikg project."""
from emikg_interfaces.record import Record
from emikg_interfaces.core import Sample, Taxon, User, Spectrum, SpectraCollection, Task, TaskType, Authored
from emikg_interfaces.from_identifier import FromIdentifier, IdentifierNotFound

__all__ = [
    "Sample",
    "Taxon",
    "User",
    "Spectrum",
    "Record",
    "SpectraCollection",
    "FromIdentifier",
    "IdentifierNotFound",
    "Task",
    "TaskType",
    "Authored",
]