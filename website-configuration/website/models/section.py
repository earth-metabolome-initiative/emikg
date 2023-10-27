"""Abstract interface describing an object whose page contains sections."""

from typing import List, Optional, Type, Union
from emikg_interfaces import Authored, Record
from humanize import naturaldelta
from flask import render_template


class Pin:
    """Abstract interface describing a pin."""

    def get_pin(self) -> Optional[str]:
        """Return section pin."""
        raise NotImplementedError(
            "Abstract method 'get_pin' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )


class FontAwesomePin(Pin):
    """Abstract interface describing a font awesome pin."""

    def __init__(
        self,
        classes: Union[List[str], str],
        color: str,
        name: str,
        action: Optional[str] = None,
    ) -> None:
        if isinstance(classes, str):
            classes = [classes]
        self._color = color
        self._classes = classes
        self._name = name
        self._action = action

    def get_classes(self) -> List[str]:
        """Return classes."""
        return self._classes

    def get_class(self) -> str:
        """Return joined classes."""
        return " ".join(self.get_classes())

    def get_color(self) -> str:
        """Return color."""
        return self._color

    def get_name(self) -> str:
        """Return name."""
        return self._name

    def has_action(self) -> bool:
        """Return whether the pin has an action."""
        return self._action is not None

    def get_action(self) -> str:
        """Return action."""
        return self._action

    def get_pin(self) -> Optional[str]:
        """Return section pin."""
        return render_template("font_awesome_pin.html", pin=self)


class FailurePin(FontAwesomePin):
    """Abstract interface describing a failure pin."""

    def __init__(self) -> None:
        super().__init__(
            classes=["fa-solid", "fa-house-fire"], color="red", name="Failure"
        )


class SuccessPin(FontAwesomePin):
    """Abstract interface describing a success pin."""

    def __init__(self) -> None:
        super().__init__(
            classes=["fa-solid", "fa-square-check"], color="green", name="Success"
        )

class RunningPin(FontAwesomePin):
    """Abstract interface describing a running pin."""

    def __init__(self) -> None:
        super().__init__(
            classes=["fa-solid", "fa-person-running"], color="orange", name="Running"
        )

class PendingPin(FontAwesomePin):
    """Class describing a pending pin."""

    def __init__(self) -> None:
        super().__init__(classes=["fa-solid", "fa-moon"], color="blue", name="Pending")

class DeletePin(FontAwesomePin):
    """Class describing a delete pin."""

    def __init__(self, root: str, identifier: int) -> None:
        super().__init__(
            classes=["fa-solid", "fa-trash-alt"],
            color="red",
            name="Delete",
            action=f"/{root}/delete/{identifier}",
        )

class CreatedByBotPin(FontAwesomePin):
    """Class describing a created by bot pin."""

    def __init__(self) -> None:
        super().__init__(
            classes=["fa-solid", "fa-robot"], color="blue", name="Created by bot"
        )

class OnlinePin(FontAwesomePin):
    """Class describing an online pin."""

    def __init__(self) -> None:
        super().__init__(
            classes=["fa-solid", "fa-wifi", "fa-1x"], color="green", name="Online"
        )

class NewUserPin(FontAwesomePin):
    """Class describing a new user pin."""

    def __init__(self) -> None:
        super().__init__(
            classes=["fa-solid", "fa-user-graduate"], color="green", name="This user just joined the community!"
        )

class TimeRecordPin(FontAwesomePin):
    """Class describing a time record pin."""

    def __init__(self, time_required_in_seconds: int, average_time_required_in_seconds: int, completed: bool) -> None:
        # We compose the pin name, which depending on whether the record is completed or not, will be different.
        # In both instances, the time required in seconds are converted to a human readable format using the
        # humanize function naturaldelta. In the description we show both the time required for the record and
        # the average time required for the record, so that the user can compare the two.

        humanized_time_required = naturaldelta(time_required_in_seconds)
        humanized_average_time_required = naturaldelta(average_time_required_in_seconds)

        if completed:
            name = f"Completed in {humanized_time_required} (average: {humanized_average_time_required})"
        else:
            name = f"Time required so far: {humanized_time_required} (average completion: {humanized_average_time_required})"

        super().__init__(
            classes=["fa-solid", "fa-clock"], color="blue", name=name
        )

class RecordBadge:
    """Abstract interface describing a record badge."""

    def get_record_badge(self) -> Optional[str]:
        """Return section record badge."""
        return render_template("badge.html", record=self)

    def has_pins(self) -> bool:
        """Return whether the record has pins."""
        return False

    def get_pins(self) -> List[Type["Pin"]]:
        """Return pins."""
        return []


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
    def get_section_content(
        page: Type["RecordPage"], section_type: Type["Section"]
    ) -> str:
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
    def get_records(
        page: Type["RecordPage"], number_of_records: int
    ) -> List[Type[RecordBadge]]:
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
