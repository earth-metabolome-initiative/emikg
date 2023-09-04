"""Module providing an abstract factory with a connection to the database."""


class AbstractFactory:
    """Abstract factory class to create objects."""

    def __init__(self, database_connection):
        """Initialize the factory with a connection to the database."""
        self._database_connection = database_connection

    def _build(self):
        """Build a Sample class."""
        raise NotImplementedError(
            "The _build method of the AbstractFactory class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class."
        )

    def build(self):
        """Build a Sample class."""
        return self._build()
