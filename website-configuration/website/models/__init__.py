"""Submodule providing database proxy classes that concretely implement the interfaces from emikg_interfaces."""

from website.models.core import User, Taxon, Task, Document
from website.models.section import RecordPage

__all__ = [
    "User",
    "Taxon",
    "Task",
    "RecordPage",
    "Document"
]
