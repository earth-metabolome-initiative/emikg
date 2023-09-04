"""Module providing the abstract Enricher class for extending the metadata of a Sample class."""
from typing import Type
from enpkg_website.samples import AbstractSample


class AbstractEnricher:
    """Abstract Enricher class for extending the metadata of a Sample class."""

    def __init__(self) -> None:
        pass

    @classmethod
    def repository_name(cls) -> str:
        """Name of the repository providing these specific metadata."""
        raise NotImplementedError(
            "The repository_name method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {cls.__class__.__name__} class."
        )

    def _can_enrich(self, sample: Type[AbstractSample]) -> bool:
        """Returns whether the Enricher can enrich the metadata of the Sample class.

        Parameters
        ----------
        sample : Sample
            Sample class to enrich.
        """
        raise NotImplementedError(
            "The _can_enrich method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class."
        )

    def _enrich(self, sample: Type[AbstractSample]) -> Type[AbstractSample]:
        """Enrich the metadata of a Sample class.

        Parameters
        ----------
        sample : Sample
            Sample class to enrich.
        """
        raise NotImplementedError(
            "The enrich method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class. "
            f"This class should retrieve the metadata relative to the repository {self.repository_name()}."
        )

    def enrich(self, sample: Type[AbstractSample]) -> Type[AbstractSample]:
        """Enrich the metadata of a Sample class.

        Parameters
        ----------
        sample : Sample
            Sample class to enrich.
        """
        if not self._can_enrich(sample):
            return sample
        return self._enrich(sample)
