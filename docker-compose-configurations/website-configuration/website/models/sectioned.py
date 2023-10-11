"""Abstract interface describing an object whose page contains sections."""

from typing import List
from emikg_interfaces.record import Record


class Section:
    def get_title(self) -> str:
        """Return section title."""
        raise NotImplementedError(
            "Abstract method 'get_title' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_content(self) -> str:
        """Return section content."""
        raise NotImplementedError(
            "Abstract method 'get_content' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_records(self) -> List[Record]:
        """Return section records."""
        raise NotImplementedError(
            "Abstract method 'get_records' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )


class Sectioned:
    def get_sections(self) -> List[Section]:
        """Return sections."""
        raise NotImplementedError(
            "Abstract method 'get_sections' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
