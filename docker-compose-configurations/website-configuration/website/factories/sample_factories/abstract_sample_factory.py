"""Module providing the abstract sample Factory class for creating Sample classes."""

from typing import Type, Optional
from enpkg_website.samples import AbstractSample


class AbstractSampleFactory:
    """Abstract sample Factory class for creating Sample classes."""

    def __init__(
        self,
        connection: "Connection"
    ) -> None:
        self._connection = connection
        self._sample_id: Optional[str] = None
        self._source_id: Optional[str] = None

    def set_sample_id(self, sample_id: str) -> None:
        """Set the sample ID."""
        self._sample_id = sample_id

    def set_source_id(self, source_id: str) -> None:
        """Set the source ID."""
        self._source_id = source_id

    def _build(self) -> Type[AbstractSample]:
        """Build a Sample class."""
        raise NotImplementedError(
            "The _build method of the AbstractSampleFactory class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class."
        )
        
    def build(self) -> Type[AbstractSample]:
        """Build a Sample class."""
        if self._sample_id is None:
            raise ValueError(
                "The sample ID must be set before building a Sample class. "
                "This can be done by calling the set_sample_id method of the AbstractSampleFactory class."
            )
        
        if self._source_id is None:
            raise ValueError(
                "The source ID must be set before building a Sample class. "
                "This can be done by calling the set_source_id method of the AbstractSampleFactory class."
            )

        return self._build()