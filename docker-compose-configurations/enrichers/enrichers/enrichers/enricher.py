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
from typing import Type
from time import sleep
from .enrichable import Enrichable
from .models import EnrichmentTask, Enricher as EnricherModel


class Enricher:
    """Abstract Enricher class for extending the metadata of a enrichable class."""

    def __init__(self) -> None:
        """Initialize the enricher object."""
        # Create the enricher entry in the enrichers table
        # if it does not already exist. An enricher is uniquely
        # identified by its name.
        enricher = EnricherModel.query.filter_by(name=self.name()).first()
        if enricher is None:
            enricher = EnricherModel(name=self.name())
            enricher.save()
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

    def _can_enrich(self, enrichable: Type[Enrichable]) -> bool:
        """Returns whether the Enricher can enrich the metadata of the enrichable class.

        Parameters
        ----------
        enrichable: Type[Enrichable]
            enrichable class to enrich.
        """
        raise NotImplementedError(
            "The _can_enrich method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class."
        )

    def _enrich(self, enrichable: Type[Enrichable], task: EnrichmentTask):
        """Enrich the metadata of a enrichable class.

        Parameters
        ----------
        enrichable: Type[Enrichable]
            enrichable class to enrich.
        """
        raise NotImplementedError(
            "The enrich method of the Enricher class must be implemented by a subclass. "
            f"This was not done for the {self.__class__.__name__} class. "
            f"This class should retrieve the metadata relative to the repository {self.repository()}."
        )

    def _create_new_task(self, enrichable: Type[Enrichable]) -> EnrichmentTask:
        """Create a new task for the enricher.

        Implementative details
        ----------------------
        This method creates a new entry in the enrichment_tasks table and returns the corresponding
        EnrichmentTask object. The status of the task is set to PENDING.

        In the child classes, this method may be extended so as to create a new entry in the
        enricher-specific table that may contain foreign keys, such as the taxon_enrichment_tasks table.
        """
        # Create a new entry in the enrichment_tasks table
        enrichment_task = EnrichmentTask(
            enricher_id=self.id,
        )
        return enrichment_task

    def _task_can_start(
        self, enrichable: Type[Enrichable], task: EnrichmentTask
    ) -> bool:
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

    def enrich(self, enrichable: Type[Enrichable]):
        """Enrich the metadata of a enrichable class.

        Parameters
        ----------
        enrichable: Type[Enrichable]
            enrichable class to enrich.
        """
        assert issubclass(enrichable, Enrichable), (
            f"The enrichable argument of the enrich method of the Enricher class must be a subclass of Enrichable. "
            f"The {enrichable.__class__.__name__} class is not a subclass of Enrichable."
        )
        if not self._can_enrich(enrichable):
            raise ValueError(
                f"The enricher {self.name()} cannot enrich the {enrichable.__class__.__name__} class."
            )

        task = self._create_new_task(enrichable)

        while not self._task_can_start(enrichable, task):
            sleep(self._get_sleep_time_between_start_attempts())

        task.start()

        self._enrich(enrichable, task)
