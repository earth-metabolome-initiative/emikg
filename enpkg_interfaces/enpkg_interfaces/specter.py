"""Abstract interface for specter objects."""
from typing import Type

class Specter:
    """Abstract class to represent a specter."""

    def __init__(self, specter_id: int) -> None:
        """Initialize specter object.
        
        Parameters
        ----------
        specter_id : int
            specter ID.

        Raises
        ------
        ValueError
            If the specter ID does not exist.
        """
        if not Specter.is_valid_specter_id(specter_id):
            raise ValueError(
                f"Specter ID #{specter_id} does not exist."
            )
        
        self._specter_id = specter_id

    @staticmethod
    def is_valid_specter_id(specter_id: int) -> bool:
        """Check if specter ID exists.

        Parameters
        ----------
        specter_id : int
            specter ID.

        Returns
        -------
        bool
            True if specter ID exists, False otherwise.
        """
        raise NotImplementedError(
            "Abstract method 'is_valid_specter_id' should be implemented in derived class. "
        )
    
    @staticmethod
    def is_valid_specter_name(specter_name: str) -> bool:
        """Check if specter name exists.

        Parameters
        ----------
        specter_name : str
            specter name.

        Returns
        -------
        bool
            True if specter name exists, False otherwise.
        """
        raise NotImplementedError(
            "Abstract method 'is_valid_specter_name' should be implemented in derived class. "
        )

    def get_specter_id(self) -> int:
        """Return specter ID."""
        return self._specter_id

    def get_parent_sample(self) -> Type["Sample"]:
        """Return parent sample."""
        raise NotImplementedError(
            "Abstract method '_get_parent_sample' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
    
    def get_author_user_id(self) -> int:
        """Return author user ID."""
        raise NotImplementedError(
            "Abstract method 'get_author_user_id' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )