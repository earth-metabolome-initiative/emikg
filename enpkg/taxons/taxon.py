"""Module providing class to model a Taxon and its associated metadata.

Implementative details
----------------------

The Taxon class describes the taxonomic classification of the organism (or set of organisms) sampled.
It can be precise (e.g. down to the species level) or general (e.g. up to the phylum level). 

"""


class Taxon:
    """Class to model a Taxon and its associated metadata."""

    def __init__(self, name: str) -> None:
        self._name = name

    def name(self) -> str:
        """Returns the name of the taxon."""
        return self._name
