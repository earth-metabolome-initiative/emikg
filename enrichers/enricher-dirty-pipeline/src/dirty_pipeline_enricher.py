"""Concrete implementation for the Dirty Pipeline enricher.

Implementative details
----------------------
The dirty pipeline enricher is an enricher based on the original dirty pipeline
built as a sequence of python repositories. This enricher is meant to be a temporary
solution to provide the complete enrichment for a given user provided payload, but
it really isn't meant to be a long term solution.

We want a precise clockwork swiss army knife for the enrichment, and the dirty pipeline
is more like a pipebomb. 
"""
from typing import List

from alchemy_wrapper.models import DataPayload, Task, Document, TaskRelatedDocuments
from enrichers import Enricher
import shutil


class DirtyPipelineEnricher(Enricher):
    """Concrete implementation for the Dirty Pipeline enricher."""

    @classmethod
    def repository(cls) -> str:
        """Name of the repository providing these specific metadata."""
        return "Dirty Pipeline"

    @classmethod
    def name(cls) -> str:
        """Name of the enricher."""
        return "Dirty Pipeline"

    def _can_enrich(self, enrichable: DataPayload) -> bool:
        """Returns whether the Enricher can enrich the metadata of the enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.

        Implementation details
        ----------------------
        The payloads that can be enriched by the dirty pipeline are the ones
        associated to tasks that are still PENDING.
        """
        if not isinstance(enrichable, DataPayload):
            return False
        
        return self._session.query(Task).filter_by(
            id=enrichable.task_id
        ).first().status == "PENDING"

    def _get_sleep_time_between_start_attempts(self) -> int:
        """Returns the number of seconds to wait between two start attempts."""
        return 10

    def _task_can_start(self, enrichable: DataPayload, task: Task) -> bool:
        """Returns whether the task can start.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        # A task can start if there is not already an entry in the
        # open_tree_of_life table with the same DataPayload_id.
        return self._can_enrich(enrichable)

    def _get_new_elements_to_enrich(self) -> List[DataPayload]:
        """Returns a list of new elements to enrich.
        
        Implementation details
        ----------------------
        The new elements to enrich are the ones that are associated to a task with
        status PENDING.
        """
        return self._session.query(DataPayload).join(Task, Task.id==DataPayload.task_id).filter(
            Task.status == "PENDING"
        ).all()
    
    def _create_new_task(self, enrichable: DataPayload) -> Task:
        # In the case of the data payload, there is no need
        # to create a new entry in the task table, as there is
        # already one associated to the data payload.
        return self._session.query(Task).filter_by(
            id=enrichable.task_id
        ).first()

    def _enrich(self, enrichable: DataPayload, task: Task) -> bool:
        """Enrich the metadata of a enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        # We set the status of the task associated to the enrichable to STARTED.
        path = enrichable.get_unsafe_path()

        # TODO: Implement the enrichment here.

        # TEMPORARELY we copy the original payload directly to the safe folder
        # to monkeypatch the execution of the pipeline.

        shutil.copy(path, enrichable.get_safe_path())

        # We create a new document entry in the database.
        document = Document(
            name=f"Dirty Pipeline enrichment for task {task.id}",
            description=f"Dirty Pipeline enrichment for task {task.id}",
            path=enrichable.get_safe_path(),
            user_id=self._enricher.id,
        )

        self._session.add(document)
        self._session.flush()

        # We insert a new entry for relationship between the task and the document.
        task_document = TaskRelatedDocuments(
            task_id=task.id,
            document_id=document.id,
        )

        self._session.add(task_document)

        # We set the task associated to the enrichable to SUCCESS.
        task.success()

        # We commit the changes.
        self._session.commit()

        # raise NotImplementedError("This method should be implemented in derived classes.")
        return True