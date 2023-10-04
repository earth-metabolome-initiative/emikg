"""Concrete implementation for the Open Tree of Life taxon Enricher."""
from enrichers import TaxonEnricher


class OTLEnricher(TaxonEnricher):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def repository_name(cls) -> str:
        """Name of the repository providing these specific metadata."""
        return "Open Tree of Life"

    def _can_enrich(self, enrichable) -> bool:
        """Returns whether the Enricher can enrich the metadata of the enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        return True

    def _enrich(self, enrichable):
        """Enrich the metadata of a enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        return enrichable
