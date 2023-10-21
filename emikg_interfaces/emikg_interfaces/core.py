from typing import List, Type, Optional
from .record import Record

class User(Record):
    """Abstract class to represent a user."""

    def is_administrator(self) -> bool:
        """Return True if the user is an administrator."""
        raise NotImplementedError(
            "Abstract method 'is_administrator' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    def is_moderator(self) -> bool:
        """Return True if the user is a moderator."""
        raise NotImplementedError(
            "Abstract method 'is_moderator' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    def get_taxons(self, number_of_records: int) -> List[Type["Taxon"]]:
        """Return list of taxons created by the user.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        raise NotImplementedError(
            "Abstract method 'get_taxons' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    def get_samples(self, number_of_records: int) -> List[Type["Sample"]]:
        """Return list of samples created by the user.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        raise NotImplementedError(
            "Abstract method 'get_samples' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    def get_spectra_collections(
        self, number_of_records: int
    ) -> List[Type["SpectraCollection"]]:
        """Return list of spectra collections created by the user.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        raise NotImplementedError(
            "Abstract method 'get_spectra_collections' must be implemented in subclass. "
            f"It was not implemented in {self.__class__.__name__}."
        )

    @staticmethod
    def get_root() -> str:
        """Return root for the user interface."""
        return "users"
    

class Authored:
    """Abstract interface describing the methods associated to an object with an author."""

    def get_author(self) -> Type[User]:
        """Return author user."""
        raise NotImplementedError(
            "Abstract method 'get_author' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )
    
    def is_author(self, user: Type[User]) -> bool:
        """Return True if user is author."""
        return self.get_author().get_id() == user.get_id()
    
class Taxon(Record, Authored):
    """Abstract class to represent a taxon."""

    def get_samples(self, number_of_records: int) -> List[Type["Sample"]]:
        """Return list of samples.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        raise NotImplementedError(
            "Abstract method 'get_samples' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    @staticmethod
    def get_root() -> str:
        """Return root for the taxon interface."""
        return "taxons"

class Sample(Record, Authored):
    """Abstract class to represent a sample."""

    def is_derived_sample(self) -> bool:
        """Return True if sample is derived from another sample."""
        return self.get_parent_sample() is not None

    def is_primary_sample(self) -> bool:
        """Return True if sample is primary sample, i.e. not derived from another sample."""
        return not self.is_derived_sample()

    def get_parent_sample(self) -> Optional[Type["Sample"]]:
        """Return parent sample."""
        raise NotImplementedError(
            "Abstract method '_get_parent_sample' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_child_samples(self) -> List[Type["Sample"]]:
        """Return list of child samples."""
        raise NotImplementedError(
            "Abstract method 'get_child_samples' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    def get_spectra_collections(self) -> List[Type["SpectraCollection"]]:
        """Return list of spectra collections."""
        raise NotImplementedError(
            "Abstract method 'get_spectra_collections' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    @staticmethod
    def get_root() -> str:
        """Return root for the sample interface."""
        return "samples"
    
class SpectraCollection(Record, Authored):
    def get_spectra(self) -> List[Type["Spectrum"]]:
        """Return a list of spectra."""
        raise NotImplementedError(
            "SpectraCollection.get_spectra() not implemented "
            f" for {self.__class__.__name__}"
        )

    def get_sample(self) -> Type[Sample]:
        """Return sample."""
        raise NotImplementedError(
            "SpectraCollection.get_sample() not implemented "
            f" for {self.__class__.__name__}"
        )

    @staticmethod
    def get_root() -> str:
        """Return root for the spectra_collection interface."""
        return "spectra_collections"
    
class Spectrum(Record, Authored):
    """Abstract class to represent a spectrum."""

    def get_spectra_collection(self) -> SpectraCollection:
        """Return spectra collection."""
        raise NotImplementedError(
            "Abstract method 'get_spectra_collection' should be implemented in derived class. "
            f"It was not implemented in class {self.__class__.__name__}."
        )

    @staticmethod
    def get_root() -> str:
        """Return root for the spectrum interface."""
        return "spectra"
    
class TaskType(Record, Authored):
    """Abstract interface to describe a generic task type."""

    @staticmethod
    def get_root() -> str:
        """Return root for the spectrum interface."""
        return "task_types"

class Task(Record, Authored):
    """Abstract interface to describe a generic task.

    Examples
    --------
    A task may be a set of instructions to be executed by an enricher, such
    as retrieving additional information for a sample. This object may be
    simple, i.e. composed of a single task, or complex, i.e. composed of a
    chain of tasks that should be executed in a specific order.
    """

    @staticmethod
    def get_root() -> str:
        """Return root for the spectrum interface."""
        return "tasks"
    