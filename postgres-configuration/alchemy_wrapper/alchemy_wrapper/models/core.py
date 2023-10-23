"""SQLAlchemy model for the user and sample tables."""

from typing import List, Optional, Type, Union
from alchemy_wrapper.database import Session
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Float,
    Enum,
    UniqueConstraint,
)

from emikg_interfaces import User as UserInterface
from emikg_interfaces import Sample as SampleInterface
from emikg_interfaces import Taxon as TaxonInterface
from emikg_interfaces import Spectrum as SpectrumInterface
from emikg_interfaces import SpectraCollection as SpectraCollectionInterface
from emikg_interfaces import Task as TaskInterface
from emikg_interfaces import TaskType as TaskTypeInterface
from emikg_interfaces import Document as DocumentInterface
from emikg_interfaces import IdentifierNotFound, FromIdentifier

import traceback
import subprocess
from alchemy_wrapper.models.administrator import Administrator
from alchemy_wrapper.models.base import Base
from alchemy_wrapper.models.moderator import Moderator
from alchemy_wrapper.models.bot import Bot
from alchemy_wrapper.models.social_profiles import SocialProfile
import os


class User(Base, UserInterface):
    """Define the User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    @staticmethod
    def from_id(identifier: int, session: Type[Session]) -> "User":
        """Return the user corresponding to the given identifier.

        Parameters
        ----------
        identifier : int
            The identifier of the user to return.

        Raises
        ------
        UserNotFound
            If the user corresponding to the given identifier is not found.
        """
        # We query the user table to get the user corresponding to the given identifier
        user = session.query(User).filter_by(id=identifier).first()
        if user is None:
            raise IdentifierNotFound(f"User with id {identifier} not found")
        return user

    def get_id(self) -> int:
        """Return the identifier of the user."""
        return self.id

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"

    def is_moderator(self, session: Type[Session]):
        """Check if user is a moderator.

        Implementation details
        ----------------------
        This method checks if the user is a moderator by checking if the user
        id appears in the moderators table.
        """
        # We query the moderators table to check if the user is a moderator
        return session.query(Moderator).filter_by(user_id=self.id).first() is not None

    def is_administrator(self, session: Type[Session]):
        """Check if user is an administrator.

        Implementation details
        ----------------------
        This method checks if the user is an administrator by checking if the user
        id appears in the administrators table.
        """
        # We query the administrators table to check if the user is an administrator
        return (
            session.query(Administrator).filter_by(user_id=self.id).first() is not None
        )

    def is_bot(self, session: Type[Session]):
        """Check if user is a bot.

        Implementation details
        ----------------------
        This method checks if the user is a bot by checking if the user
        id appears in the bots table.
        """
        # We query the bots table to check if the user is a bot
        return session.query(Bot).filter_by(user_id=self.id).first() is not None

    def delete(self):
        """Delete the user."""
        # We delete the user from the database
        session = Session()
        session.delete(self)
        session.commit()

    def has_taxons(self, session: Type[Session]) -> bool:
        """Return whether the user has taxons."""
        return session.query(Taxon).filter_by(user_id=self.id).first() is not None

    def get_taxons(
        self, number_of_records: int, session: Type[Session]
    ) -> List["Taxon"]:
        """Return list of taxons created by the user.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        # We return the most recent taxons created by the user
        return (
            session.query(Taxon)
            .filter_by(user_id=self.id)
            .order_by(Taxon.updated_at.desc())
            .limit(number_of_records)
            .all()
        )

    def has_samples(self, session: Type[Session]) -> bool:
        """Return whether the user has samples."""
        return session.query(Sample).filter_by(user_id=self.id).first() is not None

    def get_samples(
        self, number_of_records: int, session: Type[Session]
    ) -> List["Sample"]:
        """Return list of samples created by the user.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        # We return the most recent samples created by the user
        return (
            session.query(Sample)
            .filter_by(user_id=self.id)
            .order_by(Sample.updated_at.desc())
            .limit(number_of_records)
            .all()
        )

    def has_tasks(self, session: Type[Session]) -> bool:
        """Return whether the user has tasks."""
        return session.query(Task).filter_by(user_id=self.id).first() is not None

    def get_tasks(self, number_of_records: int, session: Type[Session]) -> List["Task"]:
        """Return list of tasks created by the user.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        # We return the most recent tasks created by the user
        return (
            session.query(Task)
            .filter_by(user_id=self.id)
            .order_by(Task.updated_at.desc())
            .limit(number_of_records)
            .all()
        )

    def get_social_profiles(self, session: Type[Session]) -> List[SocialProfile]:
        """Return list of socials."""
        return (
            session.query(SocialProfile).filter(SocialProfile.user_id == self.id).all()
        )

    def get_name(self) -> str:
        """Return recorded object name."""
        return f"{self.first_name} {self.last_name}"

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description


class Sample(Base, SampleInterface):
    """Define the Sample model."""

    __tablename__ = "samples"

    id = Column(Integer, primary_key=True)
    taxon_id = Column(
        Integer, ForeignKey("taxons.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altitude = Column(Float, nullable=True)
    # The derived from column is a foreign key to the sample table
    # It is used to link a sample to the sample it was derived from
    # For example, if a sample is a subsample of another sample, the derived from column
    # will be set to the id of the sample it was derived from
    # If the sample is not derived from another sample, the derived from column will be
    # set to None
    # The ondelete="SET NULL" means that if the sample it was derived from is deleted,
    # the derived from column will be set to None
    # The nullable=True means that the derived from column can be set to None
    # If the derived from column is set to None, it means that the sample is not derived
    # from another sample
    derived_from = Column(
        Integer, ForeignKey("samples.id", ondelete="SET NULL"), nullable=True
    )

    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def get_parent_sample(self) -> Optional["Sample"]:
        """Return parent sample."""
        if self.derived_from is None:
            return None
        return Sample.from_id(self.derived_from)

    def get_child_samples(self) -> List["Sample"]:
        """Return list of child samples."""
        return Session().query(Sample).filter_by(derived_from=self.id).all()

    @staticmethod
    def from_id(identifier: int) -> "Sample":
        """Return Sample instance from Sample id."""
        # We query the user table to get the user corresponding to the given identifier
        sample = Session().query(Sample).filter_by(id=identifier).first()
        if sample is None:
            raise IdentifierNotFound(f"Sample with id {identifier} not found")
        return sample

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def get_author(self, session: Type[Session]) -> User:
        """Return the author of the sample."""
        return User.from_id(self.user_id, session=session)

    def delete(self):
        """Delete the sample."""
        # We delete the sample from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description


class Taxon(Base, TaxonInterface):
    """Define the Taxon model."""

    __tablename__ = "taxons"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(255), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Taxon({self.name!r})>"

    @staticmethod
    def from_id(identifier: int) -> "Taxon":
        """Return taxon instance from taxon id."""
        # We query the user table to get the user corresponding to the given identifier
        taxon = Session().query(Taxon).filter_by(id=identifier).first()
        if taxon is None:
            raise IdentifierNotFound(f"Taxon with id {identifier} not found")
        return taxon

    def get_id(self) -> int:
        """Return taxon id."""
        return self.id

    def delete(self):
        """Delete the user."""
        # We delete the user from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_samples(self, session: Type[Session]) -> List[Sample]:
        """Return list of samples."""
        return session.query(Sample).filter_by(taxon_id=self.id).all()

    def get_author(self, session: Type[Session]) -> User:
        """Return author."""
        return session.query(User).filter_by(id=self.user_id).first()

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description

    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name


class Spectrum(Base, SpectrumInterface):
    """SQLAlchemy model for the spectrographic data."""

    __tablename__ = "spectra"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=False)
    spectra_collection_id = Column(
        Integer, ForeignKey("spectra_collection.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    @staticmethod
    def from_id(identifier: int, session: Type[Session]) -> "Spectrum":
        """Return Spectrum instance from Spectrum id."""
        # We query the user table to get the user corresponding to the given identifier
        spectrum = session.query(Spectrum).filter_by(id=identifier).first()
        if spectrum is None:
            raise IdentifierNotFound(f"Spectrum with id {identifier} not found")
        return spectrum

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def get_spectra_collection(self, session: Type[Session]) -> "SpectraCollection":
        """Return the spectra collection of the spectrum."""
        return SpectraCollection.from_id(self.spectra_collection_id, session=session)

    def get_author(self, session: Type[Session]) -> User:
        """Return the author of the spectrum."""
        return self.get_spectra_collection(session).get_author(session)

    def delete(self):
        """Delete the spectrum."""
        # We delete the spectrum from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description

    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name


class SpectraCollection(Base, SpectraCollectionInterface):
    """SQLAlchemy model for spectra_collection table."""

    __tablename__ = "spectra_collection"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    sample_id = Column(
        Integer, ForeignKey("samples.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    def get_spectra(self) -> List[Type[Spectrum]]:
        """Return a list of spectra."""
        raise NotImplementedError(
            "SpectraCollection.get_spectra() not implemented "
            f" for {self.__class__.__name__}"
        )

    def get_sample(self) -> Sample:
        """Return sample."""
        return Sample.from_id(self.sample_id)

    @staticmethod
    def from_id(identifier: int, session: Type[Session]) -> "SpectraCollection":
        """Return SpectraCollection instance from SpectraCollection id."""
        # We query the user table to get the user corresponding to the given identifier
        spectra_collection = (
            session.query(SpectraCollection).filter_by(id=identifier).first()
        )
        if spectra_collection is None:
            raise IdentifierNotFound(
                f"SpectraCollection with id {identifier} not found"
            )
        return spectra_collection

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def delete(self):
        """Delete the spectra collection."""
        # We delete the spectra collection from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_author(self, session: Type[Session]) -> User:
        """Return the author of the spectrum."""
        return User.from_id(self.user_id, session=session)

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description

    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name


class TaskType(Base, TaskTypeInterface):
    """Define the TaskType model."""

    __tablename__ = "task_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=False)

    @staticmethod
    def from_id(identifier: int, session: Type[Session]) -> "TaskType":
        """Return TaskType instance from TaskType id."""
        # We query the user table to get the user corresponding to the given identifier
        task_type = session.query(TaskType).filter_by(id=identifier).first()
        if task_type is None:
            raise IdentifierNotFound(f"TaskType with id {identifier} not found")
        return task_type

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TaskType({self.name!r})>"

    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description


class Task(Base, TaskInterface):
    """Define the Task model."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    status = Column(
        Enum("PENDING", "STARTED", "SUCCESS", "FAILURE", name="status"),
        nullable=False,
        default="PENDING",
    )
    task_type_id = Column(
        Integer,
        ForeignKey("task_types.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Task({self.id!r})>"
    
    def restart(self, session: Type[Session]):
        """Restart the task."""
        self.status = "PENDING"
        session.commit()

    def start(self, session: Type[Session]):
        """Start the task."""
        self.status = "STARTED"
        session.commit()

    def success(self, session: Type[Session]):
        """Finish the task successfully."""
        self.status = "SUCCESS"
        session.commit()

    def failure(self, session: Type[Session], reason: Optional[Union[str, Exception]] = None):
        """Finish the task with a failure."""
        if self.status == "FAILURE":
            return
        self.status = "FAILURE"
        session.commit()
        if reason is None:
            return

        if isinstance(reason, subprocess.CalledProcessError):
            reason = (
                f"Command {reason.cmd} returned non-zero exit status {reason.returncode}. "
                f"Output: {reason.output}, {reason.stderr}."
            )

        if isinstance(reason, Exception):
            reason = traceback.format_exc()

        # We create a new Document associated to the task
        path = f"/app/safe/tasks/{self.id}/failure.txt"

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True,
        )

        with open(path, "w", encoding="utf8") as file:
            file.write(reason)

        document = Document(
            name=f"Task {self.id} failure log",
            description=f"Reason for the task #{self.id} failure.",
            path=path,
            user_id=self.user_id,
        )

        session.add(document)
        session.flush()

        task_related_documents = TaskRelatedDocument(
            document_id=document.id,
            task_id=self.id,
        )

        session.add(task_related_documents)

        session.commit()


    def get_status(self) -> str:
        """Return task status."""
        return self.status

    def has_failed(self) -> bool:
        """Return whether the task has failed."""
        return self.status == "FAILURE"
    
    def has_started(self) -> bool:
        """Return whether the task has started."""
        return self.status == "STARTED"

    def has_parent_task(self, session: Type[Session]) -> bool:
        """Return whether the task has a parent task."""
        return (
            session.query(DerivedTask).filter_by(derived_task_id=self.id).first()
            is not None
        )

    def get_parent_task(self, session: Type[Session]) -> Optional["Task"]:
        """Return parent task."""
        return (
            session.query(Task)
            .join(DerivedTask, DerivedTask.parent_task_id == Task.id)
            .filter_by(derived_task_id=self.id)
            .first()
        )
    
    def has_derived_tasks(self, session: Type[Session]) -> bool:
        """Return whether the task has derived tasks."""
        return (
            session.query(DerivedTask).filter_by(parent_task_id=self.id).first()
            is not None
        )

    def get_derived_tasks(
        self, session: Type[Session], number_of_records: int
    ) -> List["Task"]:
        """Return list of child tasks."""
        return (
            session.query(Task)
            .join(DerivedTask, DerivedTask.derived_task_id == Task.id)
            .filter_by(parent_task_id=self.id)
            .order_by(Task.updated_at.desc())
            .limit(number_of_records)
            .all()
        )

    def get_name(self, session: Type[Session]) -> str:
        """Return recorded object name, associated to the task type."""
        return self.get_task_type(session=session).get_name()

    def get_description(self, session: Type[Session]) -> str:
        """Return recorded object description, associated to the task type."""
        return self.get_task_type(session=session).get_description()

    def get_author(self, session: Type[Session]) -> User:
        """Return the author of the task."""
        return User.from_id(self.user_id, session=session)

    def get_task_type(self, session: Type[Session]) -> TaskType:
        """Return the task type of the task."""
        return TaskType.from_id(self.task_type_id, session=session)

    @staticmethod
    def from_id(identifier: int, session: Type[Session]) -> "Task":
        """Return Task instance from Task id."""
        # We query the user table to get the user corresponding to the given identifier
        task = session.query(Task).filter_by(id=identifier).first()
        if task is None:
            raise IdentifierNotFound(f"Task with id {identifier} not found")
        return task

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id

    def has_documents(self, session: Type[Session]) -> bool:
        """Return whether the task has documents."""
        return (
            session.query(TaskRelatedDocument).filter_by(task_id=self.id).first()
            is not None
        )

    def get_documents(
        self, session: Type[Session], number_of_records: int
    ) -> List["Document"]:
        """Return list of documents."""
        return (
            session.query(Document)
            .join(TaskRelatedDocument, TaskRelatedDocument.document_id == Document.id)
            .filter_by(task_id=self.id)
            .order_by(Document.updated_at.desc())
            .limit(number_of_records)
            .all()
        )


class Document(Base, DocumentInterface):
    """Define the Document model."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=False)
    path = Column(String(255), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def get_name(self) -> str:
        """Return recorded object name."""
        return self.name

    def get_description(self) -> str:
        """Return recorded object description."""
        return self.description

    @staticmethod
    def from_id(identifier: int, session: Type[Session]) -> "Document":
        """Return Document instance from Document id."""
        # We query the user table to get the user corresponding to the given identifier
        document = session.query(Document).filter_by(id=identifier).first()
        if document is None:
            raise IdentifierNotFound(f"Document with id {identifier} not found")
        return document

    def get_id(self) -> int:
        """Return Sample id."""
        return self.id


class TaskRelatedDocument(Base):
    """Define relationship between tasks and documents."""

    __tablename__ = "task_related_documents"

    id = Column(Integer, primary_key=True)
    document_id = Column(
        Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    task_id = Column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )

    # The combination of document id and task id have to be unique.
    __table_args__ = (UniqueConstraint("document_id", "task_id"),)


class DerivedTask(Base):
    """Define relationship between parent class and derived classes."""

    __tablename__ = "derived_tasks"

    id = Column(Integer, primary_key=True)
    parent_task_id = Column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    derived_task_id = Column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )

    # The combination of document id and task id have to be unique.
    __table_args__ = (UniqueConstraint("parent_task_id", "derived_task_id"),)
