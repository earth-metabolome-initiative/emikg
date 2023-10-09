"""Abstract interface for spectrum objects."""
from typing import Type


class Spectrum:
    """Abstract class to represent a spectrum."""

    def __init__(self, spectrum_id: int) -> None:
        """Initialize spectrum object.

        Parameters
        ----------
        spectrum_id : int
            spectrum ID.

        Raises
        ------
        ValueError
            If the spectrum ID does not exist.
        """
        if not Spectrum.is_valid_spectrum_id(spectrum_id):
            raise ValueError(f"Spectrum ID #{spectrum_id} does not exist.")

        self._spectrum_id = spectrum_id

    @staticmethod
    def is_valid_spectrum_id(spectrum_id: int) -> bool:
        """Check if spectrum ID exists.

        Parameters
        ----------
        spectrum_id : int
            spectrum ID.

        Returns
        -------
        bool
            True if spectrum ID exists, False otherwise.
        """
        raise NotImplementedError(
            "Abstract method 'is_valid_spectrum_id' should be implemented in derived class. "
        )

    @staticmethod
    def is_valid_spectrum_name(spectrum_name: str) -> bool:
        """Check if spectrum name exists.

        Parameters
        ----------
        spectrum_name : str
            spectrum name.

        Returns
        -------
        bool
            True if spectrum name exists, False otherwise.
        """
        raise NotImplementedError(
            "Abstract method 'is_valid_spectrum_name' should be implemented in derived class. "
        )

    def get_spectrum_id(self) -> int:
        """Return spectrum ID."""
        return self._spectrum_id

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
