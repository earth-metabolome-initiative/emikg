"""Abstract interface describing an object whose page contains sections."""

from typing import List, Optional, Type
from emikg_interfaces.record import Record
from flask import render_template

class RecordBadge:

    def get_record_badge(self) -> Optional[str]:
        """Return section record badge."""
        return render_template("badge.html", record=self)

class Section:
    def get_title(self) -> str:
        """Return section title."""
        raise NotImplementedError(
            "Abstract method 'get_title' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
    
    def get_section_header(self) -> str:
        """Return section header."""
        raise NotImplementedError(
            "Abstract method 'get_section_header' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_section_content(self) -> str:
        """Return section content."""
        return render_template("section.html", section=self)
    
    def get_records(self, number_of_records: int) -> List[Type[RecordBadge]]:
        """Return section records.
        
        Parameters
        ----------
        number_of_records : int
            Number of records to return.
        """
        raise NotImplementedError(
            "Abstract method 'get_records' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )


class RecordPage(Record):
    def get_sections(self) -> List[Section]:
        """Return sections."""
        raise NotImplementedError(
            "Abstract method 'get_sections' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_record_content(self) -> str:
        """Return sectioned record content."""
        return render_template("record.html", record=self)