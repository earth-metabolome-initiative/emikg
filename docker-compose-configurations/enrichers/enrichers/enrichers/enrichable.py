"""Module describing the enrichable interface."""

class Enrichable:
    """Abstract class for enrichable objects."""

    def __init__(self) -> None:
        pass

    def can_be_enriched(self) -> bool:
        """Returns whether the enrichable object can be enriched."""
        raise NotImplementedError(
            "The can_be_enriched method of the Enrichable class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class."
        )