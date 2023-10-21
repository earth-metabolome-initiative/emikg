"""Abstract interface describing an object whose page contains sections."""

from typing import List, Optional, Type
from emikg_interfaces import Authored, Record
from flask import render_template

class RecordBadge:
    """Abstract interface describing a record badge."""

    def get_record_badge(self) -> Optional[str]:
        """Return section record badge."""
        return render_template("badge.html", record=self)

class Section:
    """Abstract interface describing a section of a record page in the website."""

    @staticmethod
    def get_section_title(page: Type["RecordPage"]) -> str:
        """Return section title."""
        raise NotImplementedError(
            "Abstract method 'get_section_title' should be implemented in derived class. "
        )

    @staticmethod
    def get_section_header(page: Type["RecordPage"]) -> str:
        """Return section header."""
        raise NotImplementedError(
            "Abstract method 'get_section_header' should be implemented in derived class. "
        )

    @staticmethod
    def get_section_content(page: Type["RecordPage"], section_type: Type["Section"]) -> str:
        """Return section content."""
        return render_template("section.html", page=page, section=section_type)
    
    @staticmethod
    def has_records(page: Type["RecordPage"]) -> bool:
        """Return whether the section has records."""
        raise NotImplementedError(
            "Abstract method 'has_records' should be implemented in derived class. "
            f"It was not implemented in main page {page.__class__.__name__}."
        )

    @staticmethod
    def get_records(page: Type["RecordPage"], number_of_records: int) -> List[Type[RecordBadge]]:
        """Return section records.
        
        Parameters
        ----------
        number_of_records : int
            Number of records to return.
        """
        raise NotImplementedError(
            "Abstract method 'get_records' should be implemented in derived class. "
            f"It was not implemented in main page {page.__class__.__name__}."
        )

class RecordPage(Record):
    """Abstract interface describing an object whose page contains sections."""

    def get_sections(self) -> List[Section]:
        """Return sections."""
        raise NotImplementedError(
            "Abstract method 'get_sections' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
    
    def is_authored(self) -> bool:
        """Return whether the record is authored."""
        return issubclass(self.__class__, Authored)