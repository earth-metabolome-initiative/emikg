"""Concretely implements the proxy user and taxon interface using SQLAlchemy."""
from flask import session
from typing import List, Type, Optional
from flask import render_template
from emikg_interfaces import User as UserInterface
from emikg_interfaces import Task as TaskInterface
from emikg_interfaces import Taxon as TaxonInterface
from emikg_interfaces import Sample as SampleInterface
from emikg_interfaces import Document as DocumentInterface
from emikg_interfaces.from_identifier import IdentifierNotFound
from alchemy_wrapper.models import User as UsersTable
from alchemy_wrapper.models import Sample as SampleTable
from alchemy_wrapper.models import Taxon as TaxonTable
from alchemy_wrapper.models import Task as TaskTable
from alchemy_wrapper.models import Document as DocumentTable
from alchemy_wrapper.models import ORCID
from .section import (
    RecordPage,
    Section,
    RecordBadge,
    Pin,
    FailurePin,
    SuccessPin,
    RunningPin,
    PendingPin,
    DeletePin,
    CreatedByBotPin,
    TimeRecordPin,
)
from ..exceptions import APIException, NotLoggedIn, Unauthorized
from ..application import db


class Tasks(Section, RecordPage):
    @staticmethod
    def get_root() -> str:
        """Return the root of the page."""
        return Task.get_root()

    def get_title(self) -> str:
        """Return the title of the user."""
        return "Tasks"

    def get_url(self) -> str:
        """Return the URL of the user."""
        lang = session.get("lang", "en")
        return f"/{lang}/{self.get_root()}"

    def get_description(self) -> str:
        """Return the description of the user."""
        return "In this page you can see the recent tasks. <a href='/upload/'>You can create a new upload task here.</a>"

    def has_pins(self) -> bool:
        """Return whether the user has pins."""
        return False

    def get_sections(self) -> List[Section]:
        return [Task]

    def has_tasks(self) -> bool:
        """Return whether there are tasks in the DB."""
        return not TaskTable.is_empty(session=db.session)

    def get_tasks(self, number_of_records: int = 10) -> List[TaskInterface]:
        """Return the tasks of the user."""
        return [
            Task(task)
            for task in TaskTable.get_tasks(
                session=db.session, number_of_records=number_of_records
            )
        ]


class User(UserInterface, RecordPage, Section):
    """Concrete implementation of the user interface for Flask."""

    def __init__(self, user: UsersTable):
        """Initialize the user object from a user ID."""
        self._user = user

    @staticmethod
    def from_id(identifier: int) -> "User":
        """Return a user object from a user ID."""
        return User(UsersTable.from_id(identifier, session=db.session))

    def get_id(self) -> int:
        """Return the user ID."""
        return self._user.get_id()

    @staticmethod
    def from_flask_session() -> "User":
        """Return a user object from the Flask session."""
        try:
            return User.from_id(User.session_user_id())
        except IdentifierNotFound:
            User.logout()

    @staticmethod
    def from_orcid(
        orcid: str,
        first_name: str,
        last_name: str,
        description: Optional[str],
    ) -> "User":
        """Return a user object from an ORCID.

        Parameters
        ----------
        orcid : str
            ORCID Identifier of the shape "0000-0000-0000-0000".
        first_name : str
            First name.
        last_name : str
            Last name.
        description : str
            Description.

        Implementation details
        ----------------------
        The method looks up whether the ORCID exists in the orcid
        table of the database. If it does, we create a new user object
        from the user ID associated with the ORCID. If it does not, then
        we are currently creating a new user. We insert a new user in the
        users table, and return a new user object from the user ID of the
        newly inserted user. In the same transaction, we also insert the
        ORCID in the orcid table alongside the user ID. The transactional
        aspect is important, as it ensures that the ORCID is inserted only
        if the user is successfully inserted.
        Finally, we return a new user object from the user ID of the newly
        inserted user.
        """
        # To execute this operation, the user must not be already logged in.
        if User.is_authenticated():
            raise APIException("User is already logged in.")

        # We check whether the ORCID exists in the orcid table of the database.
        user = ORCID.get_or_insert_user_from_orcid(
            orcid,
            first_name=first_name,
            last_name=last_name,
            description=description,
            session=db.session,
        )

        # We add the user ID to the Flask session.
        session["user_id"] = user.id

        # Finally, we return a new user object from the user ID of the newly
        # inserted user.
        return User.from_id(user.id)

    @staticmethod
    def logout() -> None:
        """Logout the user.

        Implementation details
        ----------------------
        The method removes the user ID from the Flask session.
        """
        session.pop("user_id", None)

    @staticmethod
    def is_authenticated() -> bool:
        """Return whether the user is authenticated."""
        return "user_id" in session

    @staticmethod
    def session_user_id() -> int:
        """Return a user id from the Flask session."""
        if not User.is_authenticated():
            raise NotLoggedIn()
        return session.get("user_id")

    def is_session_user(self) -> bool:
        """Return whether the current user instance is the session user."""
        return self.get_id() == User.session_user_id()

    @staticmethod
    def get_session_user_language() -> str:
        """Return the language of the session user."""
        return session.get("lang", "en")

    @staticmethod
    def must_be_administrator() -> None:
        """Raise ValueError if the user is not an administrator."""
        if not User.from_flask_session().is_administrator():
            raise Unauthorized()

    @staticmethod
    def must_be_moderator() -> None:
        """Raise ValueError if the user is not an moderator."""
        if not User.from_flask_session().is_moderator():
            raise Unauthorized()

    def get_description(self) -> str:
        """Return the user description."""
        return self._user.get_description()

    def get_name(self) -> str:
        """Return the user name."""
        return self._user.get_name()

    def is_administrator(self) -> bool:
        """Return whether the user is an administrator."""
        return self._user.is_administrator(session=db.session)

    def is_moderator(self) -> bool:
        """Return whether the user is a moderator."""
        return self._user.is_moderator(session=db.session)

    def is_bot(self) -> bool:
        """Return whether the user is a bot."""
        return self._user.is_bot(session=db.session)

    def is_new(self) -> bool:
        """Return whether the user is new."""
        return self._user.is_new(session=db.session)

    def has_pins(self) -> bool:
        """Return whether the user has pins."""
        return False

    def delete(self):
        """Delete the user.

        Raises
        ------
        Unauthorized
            If the user is not an administrator.
            If the user requesting the deletion is not the user being deleted.

        Implementative details
        ----------------------
        This method is implemented by deleting the user from the database, i.e.
        by deleting from the "users" table the row whose primary ID is equal
        to the ID of the current user instance.
        """
        # If the current user is NOT the session user, then
        if not self.is_session_user():
            # The current user session must be an administrator
            User.must_be_administrator()

        # If the current user is the session user, or is an administrator,
        # then delete the user from the database
        self._user.delete()

    def get_sections(self) -> List[Section]:
        """Return sections."""
        return [Task, Taxon, Sample]

    def get_title(self) -> str:
        """Return the title of the user."""
        return self.get_name()

    def has_tasks(self) -> bool:
        """Return whether the user has tasks."""
        return self._user.has_tasks(session=db.session)

    def get_tasks(self, number_of_records: int = 10) -> List[TaskInterface]:
        """Return the tasks of the user."""
        return [
            Task(task)
            for task in self._user.get_tasks(
                session=db.session, number_of_records=number_of_records
            )
        ]

    def has_taxons(self) -> bool:
        """Return whether the user has taxons."""
        return self._user.has_taxons(session=db.session)

    def get_taxons(self, number_of_records: int = 10) -> List[TaxonInterface]:
        """Return the taxons of the user."""
        return [
            Taxon(taxon)
            for taxon in self._user.get_taxons(
                session=db.session, number_of_records=number_of_records
            )
        ]

    def has_samples(self) -> bool:
        """Return whether the user has samples."""
        return self._user.has_samples(session=db.session)

    def get_samples(self, number_of_records: int = 10) -> List[SampleInterface]:
        """Return the samples of the user."""
        return [
            Sample(sample)
            for sample in self._user.get_samples(
                session=db.session, number_of_records=number_of_records
            )
        ]


class Taxon(Section, RecordPage, TaxonInterface, RecordBadge):
    """Concrete implementation of Taxon class."""

    def __init__(self, taxon: TaxonTable):
        """Initialize the taxon object from a taxon ID."""
        self._taxon = taxon

    @staticmethod
    def from_id(identifier: int) -> "Taxon":
        """Return a taxon object from a taxon ID."""
        return Taxon(TaxonTable.from_id(identifier, session=db.session))

    def get_author(self) -> User:
        """Return the author of the taxon."""
        return User(self._taxon.get_author())

    def get_description(self) -> str:
        """Return the description of the taxon."""
        return self._taxon.get_description()

    @staticmethod
    def get_section_header(page: Type[RecordPage]) -> str:
        """Return the user section header."""
        return "Taxons"

    def get_name(self) -> str:
        """Return the name of the taxon."""
        return self._taxon.get_name()

    def get_title(self) -> str:
        """Return the title of the taxon."""
        return self.get_name()

    def get_sections(self) -> List[Section]:
        """Return sections."""
        return []

    def get_record_badge(self) -> str:
        """Return the taxon record badge."""
        return render_template("badge.html", record=self)

    def delete(self):
        """Delete the taxon."""
        user = User.from_flask_session()

        # Either the user is the author of the taxon, or the user is an admin.
        if not user.is_administrator() and not self.is_author(user):
            raise Unauthorized()

        self._taxon.delete()

    @staticmethod
    def get_section_title(page: Type["RecordPage"]) -> str:
        """Return section title."""

        if isinstance(page, User):
            return "Taxons created by this user"

        if isinstance(page, Task):
            return "Taxons associated with this task"

        raise NotImplementedError(
            "Abstract method 'get_section_title' should be "
            "implemented in derived class.  It was not implemented in "
            f"class Taxon for main class {page}"
        )

    @staticmethod
    def has_records(page: Type["RecordPage"]) -> bool:
        """Return whether the section has records."""
        if isinstance(page, User):
            return page.has_taxons()

        if isinstance(page, Task):
            return page.has_taxons()

        raise NotImplementedError(
            "Abstract method 'has_records' should be implemented in derived class Taxon. "
            f"It was not implemented in main page {page.__class__.__name__}."
        )


class Sample(SampleInterface, Section, RecordPage, RecordBadge):
    """Concrete implementation of Sample class for flask."""

    def __init__(self, sample: SampleTable):
        """Initialize the sample object from a sample ID."""
        self._sample = sample

    @staticmethod
    def from_id(identifier: int) -> "Sample":
        """Return a sample object from a sample ID."""
        return Sample(SampleTable.from_id(identifier, session=db.session))

    def get_id(self) -> int:
        """Return the sample ID."""
        return self._sample.get_id()

    def get_author(self) -> User:
        """Return the author of the sample."""
        return User(self._sample.get_author(session=db.session))

    def get_description(self) -> str:
        """Return the description of the sample."""
        return self._sample.get_description()

    @staticmethod
    def get_section_header(page: Type[RecordPage]) -> str:
        """Return the user section header."""
        return "Samples"

    def get_sections(self) -> List[Section]:
        """Return sections."""
        return []

    def get_name(self) -> str:
        """Return the name of the sample."""
        return self._sample.get_name()

    def get_title(self) -> str:
        """Return the title of the sample."""
        return self.get_name()

    @staticmethod
    def get_section_title(page: Type["RecordPage"]) -> str:
        """Return section title."""

        if isinstance(page, User):
            return "Samples created by this user"

        raise NotImplementedError(
            "Abstract method 'get_section_title' should be "
            "implemented in derived class Sample. It was not implemented in "
            f"class Sample for main class {page}"
        )

    @staticmethod
    def has_records(page: Type["RecordPage"]) -> bool:
        """Return whether the section has records."""
        if isinstance(page, User):
            return page.has_samples()

        raise NotImplementedError(
            "Abstract method 'has_records' should be implemented in derived class Sample. "
            f"It was not implemented in main page {page.__class__.__name__}."
        )


class Task(TaskInterface, Section, RecordPage, RecordBadge):
    """Concrete implementation of Task class for flask."""

    def __init__(self, task: TaskTable):
        """Initialize the task object from a task ID."""
        self._task = task

    @staticmethod
    def from_id(identifier: int) -> "Task":
        """Return a task object from a task ID."""
        return Task(TaskTable.from_id(identifier, session=db.session))

    def get_id(self) -> int:
        """Return the task ID."""
        return self._task.get_id()

    def get_author(self) -> User:
        """Return the author of the task."""
        return User(self._task.get_author(session=db.session))

    def get_description(self) -> str:
        """Return the description of the task."""
        return self._task.get_description(session=db.session)

    def get_status(self) -> str:
        """Return the status of the task."""
        return self._task.get_status()

    def has_failed(self) -> bool:
        """Return whether the task has failed."""
        return self._task.has_failed()

    def has_succeeded(self) -> bool:
        """Return whether the task has succeeded."""
        return self._task.has_succeeded()

    def has_started(self) -> bool:
        """Return whether the task is running."""
        return self._task.has_started()

    def has_completed(self) -> bool:
        """Return whether the task has completed."""
        return self.has_failed() or self.has_succeeded()

    def was_created_by_bot(self) -> bool:
        """Return whether the task was created by a bot."""
        return self._task.was_created_by_bot(session=db.session)

    def is_pending(self) -> bool:
        """Return whether the task is pending."""
        return self._task.is_pending()

    def get_average_task_type_duration(self) -> float:
        """Return the average task type duration."""
        return self._task.get_average_task_type_duration(session=db.session)

    def get_task_duration(self) -> float:
        """Return the task duration."""
        return self._task.get_task_duration()

    def has_pins(self) -> bool:
        """Return whether the task has pins."""
        return True

    @staticmethod
    def get_default() -> Tasks:
        """Return the default task page."""
        return Tasks()

    def _dispatch_status_pin(self) -> Type[Pin]:
        """Return the status pin."""
        if self.has_failed():
            return FailurePin()
        if self.has_succeeded():
            return SuccessPin()
        if self.has_started():
            return RunningPin()
        if self.is_pending():
            return PendingPin()
        raise NotImplementedError(
            "Abstract method '_dispatch_status_pin' should be implemented in derived class. "
            f"It was not implemented in main class {self.__class__.__name__}."
        )

    def get_pins(self) -> List[Type[Pin]]:
        return [
            self._dispatch_status_pin(),
            *(
                (
                    TimeRecordPin(
                        time_required_in_seconds=self.get_task_duration(),
                        average_time_required_in_seconds=self.get_average_task_type_duration(),
                        completed=self.has_completed(),
                    ),
                )
                if self.has_started()
                else ()
            ),
            *(
                (
                    DeletePin(
                        root=self.get_root(),
                        identifier=self.get_id(),
                    ),
                )
                if self.can_delete()
                else ()
            ),
            * ((CreatedByBotPin(),) if self.was_created_by_bot() else ()),
        ]

    def has_documents(self) -> bool:
        """Return whether the task has documents."""
        return self._task.has_documents(session=db.session)

    def get_documents(self, number_of_records: int = 10) -> List[DocumentInterface]:
        """Return the documents of the task."""
        return [
            Document(document)
            for document in self._task.get_documents(
                session=db.session, number_of_records=number_of_records
            )
        ]

    @staticmethod
    def get_section_header(page: Type[RecordPage]) -> str:
        """Return the user section header."""
        return "The following are up to the 10 most recent tasks."

    def get_sections(self) -> List[Section]:
        """Return sections."""
        return [Document, Task]

    def get_name(self) -> str:
        """Return the name of the task."""
        return self._task.get_name(session=db.session)

    def get_title(self) -> str:
        """Return the title of the task."""
        return self.get_name()

    def get_record_badge(self) -> str:
        """Return the task record badge."""
        return render_template("badge.html", record=self)

    def get_url(self) -> str:
        """Return the URL of the task."""
        lang = session.get("lang", "en")
        return f"/{lang}/{super().get_url()}"

    def restart(self):
        """Return whether the task restart."""
        self._task.restart(session=db.session)

    def can_delete(self) -> bool:
        """Return whether the task can be deleted."""
        if not User.is_authenticated():
            return False
        user = User.from_flask_session()
        return user.is_administrator() or self.is_author(user)

    def delete(self):
        """Delete the task."""
        if not self.can_delete():
            raise Unauthorized()
        self._task.delete(session=db.session)

    @staticmethod
    def get_section_title(page: Type["RecordPage"]) -> str:
        """Return section title."""

        if isinstance(page, User):
            return "Tasks created by this user"

        if isinstance(page, Taxon):
            return "Tasks associated with this taxon"

        if isinstance(page, Task):
            return "Derived tasks"

        if isinstance(page, Tasks):
            return "Recent tasks"

        raise NotImplementedError(
            "Abstract method 'get_section_title' should be "
            "implemented in derived class. It was not implemented in "
            f"class Task for main class {page}"
        )

    def has_derived_tasks(self) -> bool:
        """Return whether the task has derived tasks."""
        return self._task.has_derived_tasks(session=db.session)

    def has_parent_task(self) -> bool:
        """Return whether the task has a parent task."""
        return self._task.has_parent_task(session=db.session)

    def get_parent_task(self) -> "Task":
        """Return the parent task."""
        return Task(self._task.get_parent_task(session=db.session))

    @staticmethod
    def has_records(page: Type["RecordPage"]) -> bool:
        """Return whether the section has records."""
        if isinstance(page, User):
            return page.has_tasks()

        if isinstance(page, Task):
            return page.has_derived_tasks()

        if isinstance(page, Tasks):
            return page.has_tasks()

        raise NotImplementedError(
            "Abstract method 'has_records' should be implemented in derived class Task. "
            f"It was not implemented in main page {page.__class__.__name__}."
        )

    def get_derived_tasks(self, number_of_records: int) -> List["Task"]:
        """Return derived tasks."""
        return [
            Task(task)
            for task in self._task.get_derived_tasks(
                session=db.session, number_of_records=number_of_records
            )
        ]

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
        if isinstance(page, User):
            return page.get_tasks(number_of_records)

        if isinstance(page, Task):
            return page.get_derived_tasks(number_of_records)

        if isinstance(page, Tasks):
            return page.get_tasks(number_of_records)

        # if isinstance(page, Taxon):
        #     return page.get_tasks(number_of_records)

        raise NotImplementedError(
            "Abstract method 'get_records' should be implemented in derived class. "
            f"It was not implemented in main page {page.__class__.__name__}."
        )


class Document(DocumentInterface, RecordPage, RecordBadge, Section):
    """Concrete implementation of Document class for flask."""

    def __init__(self, document: DocumentTable):
        """Initialize the document object from a document ID."""
        self._document = document

    @staticmethod
    def from_id(identifier: int) -> "Document":
        """Return a document object from a document ID."""
        return Document(DocumentTable.from_id(identifier, session=db.session))

    def get_id(self) -> int:
        """Return the document ID."""
        return self._document.get_id()

    def get_author(self) -> User:
        """Return the author of the document."""
        return User(self._document.get_author(session=db.session))

    def get_description(self) -> str:
        """Return the description of the document."""
        return self._document.get_description()

    def get_name(self) -> str:
        """Return the name of the document."""
        return self._document.get_name()

    def get_title(self) -> str:
        """Return the title of the document."""
        return self.get_name()

    def get_record_badge(self) -> str:
        """Return the document record badge."""
        return render_template("badge.html", record=self)

    def can_delete(self) -> bool:
        """Return whether the document can be deleted."""
        if not User.is_authenticated():
            return False
        user = User.from_flask_session()
        return user.is_administrator() or self.is_author(user)

    def delete(self):
        """Delete the document."""
        if not self.can_delete():
            raise Unauthorized()
        self._document.delete(session=db.session)

    def has_pins(self) -> bool:
        """Return whether the document has pins."""
        return self.can_delete()

    def get_pins(self) -> List[Type[Pin]]:
        """Return pins."""
        return [
            DeletePin(
                root=self.get_root(),
                identifier=self.get_id(),
            )
            if self.can_delete()
            else None
        ]

    @staticmethod
    def get_section_header(page: Type[RecordPage]) -> str:
        """Return the user section header."""
        return "Documents"

    @staticmethod
    def get_section_title(page: Type["RecordPage"]) -> str:
        """Return section title."""

        if isinstance(page, User):
            return "Documents created by this user"

        if isinstance(page, Taxon):
            return "Documents associated with this taxon"

        if isinstance(page, Task):
            return "Documents associated with this task"

        if isinstance(page, Sample):
            return "Documents associated with this sample"

        raise NotImplementedError(
            "Abstract method 'get_section_title' should be "
            "implemented in derived class. It was not implemented in "
            f"class Document for main class {page}"
        )

    @staticmethod
    def has_records(page: Type["RecordPage"]) -> bool:
        """Return whether the section has records."""
        if isinstance(page, User):
            return page.has_documents()

        if isinstance(page, Taxon):
            return page.has_documents()

        if isinstance(page, Task):
            return page.has_documents()

        if isinstance(page, Sample):
            return page.has_documents()

        raise NotImplementedError(
            "Abstract method 'has_records' should be implemented in derived class Document. "
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
        if isinstance(page, User):
            return page.get_documents(number_of_records)

        if isinstance(page, Taxon):
            return page.get_documents(number_of_records)

        if isinstance(page, Task):
            return page.get_documents(number_of_records)

        if isinstance(page, Sample):
            return page.get_documents(number_of_records)

        raise NotImplementedError(
            "Abstract method 'get_records' should be implemented in derived class Document. "
            f"It was not implemented in main page {page.__class__.__name__}."
        )
