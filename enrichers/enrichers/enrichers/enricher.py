"""Module providing the abstract Enricher class for retrieving additional information associated to a given enrichable object.

Implementative details
----------------------
The Enricher class is an abstract class that must be extended by a subclass to be used.
Each child enricher class has a corresponding entry in the enrichers table of the database, which
identifies it uniquely by its name.

When a new task is started, the enricher object first creates an entry in the enrichment_tasks table
and since each concrete enricher tasks will have some additional characteristics, such as the Taxon
class will have the taxon_id, the enricher object will create a new entry in the corresponding table.

For instance, for the taxon enrichers, the enricher object will create a new entry in the taxon enrichment tasks
table, which will have a foreign key to the enrichment_tasks table and the taxons table.

Each task is initially set to the status of PENDING, as it may not be possible to start it immediately.
Several tasks require us to query remote services, and it may be the case that we can only send a limited
number of requests per second. When the task is started, the status is set to STARTED, and when it is
finished, the status is set to SUCCESS or FAILURE depending on whether the task was successful or not.
"""
from typing import List, Any
from time import sleep
import logging
from alchemy_wrapper import Session
from alchemy_wrapper.models import Task
from .models import Enricher as EnricherTable


class Enricher:
    """Abstract Enricher class for extending the metadata of a enrichable class."""

    def __init__(self, verbose: bool = True) -> None:
        """Initialize the enricher object."""
        self._session = Session()
        # Create the enricher entry in the enrichers table
        # if it does not already exist. An enricher is uniquely
        # identified by its name.
        self._verbose = verbose
        self._logger = logging.getLogger(self.name())
        enricher = self._session.query(EnricherTable).filter_by(name=self.name()).first()
        if enricher is None:
            enricher = EnricherTable(name=self.name())
            self._session.add(enricher)
            self._session.commit()
        self._enricher = enricher

    @property
    def id(self) -> int:
        """Id of the enricher."""
        return self._enricher.id

    @classmethod
    def name(cls) -> str:
        """Name of the enricher."""
        raise NotImplementedError(
            "The name method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {cls.__class__.__name__} class."
        )

    @classmethod
    def repository(cls) -> str:
        """Name of the repository providing these specific metadata."""
        raise NotImplementedError(
            "The repository method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {cls.__class__.__name__} class."
        )

    def _can_enrich(self, enrichable) -> bool:
        """Returns whether the Enricher can enrich the metadata of the enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        raise NotImplementedError(
            "The _can_enrich method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class."
        )

    def _enrich(self, enrichable, task: Task) -> bool:
        """Enrich the metadata of a enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.

        Returns
        -------
        Whether the enrichment was successful or not.
        """
        raise NotImplementedError(
            "The enrich method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class. "
            f"This class should retrieve the metadata relative to the repository {self.repository()}."
        )

    def _create_new_task(self, enrichable) -> Task:
        """Create a new task for the enricher.

        Implementative details
        ----------------------
        This method creates a new entry in the enrichment_tasks table and returns the corresponding
        Task object. The status of the task is set to PENDING.

        In the child classes, this method may be extended so as to create a new entry in the
        enricher-specific table that may contain foreign keys, such as the taxon_enrichment_tasks table.
        """
        # Create a new entry in the enrichment_tasks table
        enrichment_task = Task(
            enricher_id=self.id,
        )
        self._session.add(enrichment_task)
        self._session.commit()
        return enrichment_task

    def _task_can_start(self, enrichable, task: Task) -> bool:
        """Returns whether the task can be started.

        Implementative details
        ----------------------
        This method checks whether the task can be started. For instance, for the taxon enrichers,
        this method checks whether the taxon is already enriched or not.
        """
        raise NotImplementedError(
            "The _task_can_start method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class."
        )

    def _get_sleep_time_between_start_attempts(self) -> int:
        """Returns the time in milliseconds to wait between two attempts of starting the task."""
        raise NotImplementedError(
            "The _get_sleep_time_between_start_attempts method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class."
        )

    def _get_new_elements_to_enrich(self) -> List[Any]:
        """Returns list of elements to enrich."""
        raise NotImplementedError(
            "The _get_new_elements_to_enrich method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class."
        )

    def ping(self) -> None:
        """Ping the enricher."""
        self._enricher.ping()
        self._session.commit()

    def enrich(self, enrichable) -> bool:
        """Enrich the metadata of a enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        if not self._can_enrich(enrichable):
            raise ValueError(
                f"The enricher {self.name()} cannot "
                f"enrich the {enrichable.__class__.__name__} class."
            )

        task = self._create_new_task(enrichable)

        while not self._task_can_start(enrichable, task):
            sleep(self._get_sleep_time_between_start_attempts())

        task.start()
        self._session.commit()

        try:
            success = self._enrich(enrichable, task)
        except Exception:
            success = False

        if success:
            task.success()
        else:
            task.failure()

        self._session.commit()

        return success

    def enrich_all(self) -> bool:
        """Enrich the metadata of all the enrichable classes."""
        some_success = False
        for enrichable in self._get_new_elements_to_enrich():
            some_success |= self.enrich(enrichable)
        return some_success

    def start_service(self):
        """Start the enricher service."""
        minimal_sleep_time = 1
        maximal_sleep_time = 60
        sleep_time_seconds = minimal_sleep_time
        self._logger.info(f"Starting the {self.name()} enricher service.")
        while True:
            self.ping()
            some_success = self.enrich_all()
            if some_success:
                self._logger.info("Completed a round of enrichment.")
                sleep_time_seconds = max(minimal_sleep_time, sleep_time_seconds / 2)
            else:
                sleep_time_seconds = min(2 * sleep_time_seconds, maximal_sleep_time)
            sleep(sleep_time_seconds * 1000)
