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
import shutil
import os
import subprocess
from downloaders import BaseDownloader
from downloaders.extractors import AutoExtractor

from alchemy_wrapper.models import (
    DataPayload,
    Task,
    Document,
    TaskRelatedDocument,
    TaskType,
    DerivedTask,
)
from enrichers import Enricher


class DirtyPipelineEnricher(Enricher):
    """Concrete implementation for the Dirty Pipeline enricher."""

    def __init__(self):
        """Initialize the Dirty Pipeline enricher."""
        super().__init__()
        self._extractor = AutoExtractor()
        self._downloader = BaseDownloader(auto_extract=False)
        self._root = "enpkg_full/"
        self._output_path = "temporary_output/"

        self._frozen_metadata = f"./{self._root}03_enpkg_mn_isdb_isdb_taxo/db_metadata/230106_frozen_metadata.csv.gz"
        self._downloader.download(
            "https://drive.switch.ch/index.php/s/T09ictsnhv59UOy/download",
            # "https://zenodo.org/record/7534071/files/230106_frozen_metadata.csv.gz",
            self._frozen_metadata,
        )

        subprocess.run(
            [
                "python",
                f"./{self._root}03_enpkg_mn_isdb_isdb_taxo/src/adducts_formatter.py",
                "-p",
                "./db_metadata/230106_frozen_metadata.csv.gz",
            ],
            check=True,
        )

        self._downloader.download(
            "https://drive.switch.ch/index.php/s/FqZHW4Qmo1bx2mz/download",
            # "https://zenodo.org/records/8287341/files/isdb_pos_cleaned.pkl",
            "./db_spectra/isdb_pos_cleaned.pkl",
        )

        # We create the TaskType entries for the steps of the dirty pipeline.
        steps = [
            {
                "name": "Data organization",
                "description": "Ensures that the data is organized in a way that is compatible with the pipeline.",
            },
            {
                "name": "Massive ID",
                "description": "Adds massive ID to the data.",
            },
            {
                "name": "Taxonomy enhancer",
                "description": "Adds taxonomy information to the data.",
            },
            {
                "name": "ISDB annotation",
                "description": "Proceeds to ISDB annotations to the data.",
            },
            {
                "name": "Sirius/Canopus",
                "description": "Adds annotations to the data.",
            },
            {
                "name": "Chemo info fetcher",
                "description": "Adds annotations to the data.",
            },
            {
                "name": "Memo unaligned repo",
                "description": "Adds annotations to the data.",
            },
            {
                "name": "Graph builder step 1",
                "description": "First step of the graph builder.",
            },
            {
                "name": "Graph builder step 2",
                "description": "Second step of the graph builder.",
            },
            {
                "name": "Graph builder step 3",
                "description": "Third step of the graph builder.",
            },
            {
                "name": "Graph builder step 4",
                "description": "Fourth step of the graph builder.",
            },
            {
                "name": "Graph builder step 5",
                "description": "Fifth step of the graph builder.",
            },
            {
                "name": "Graph builder step 6",
                "description": "Sixth step of the graph builder.",
            },
            {
                "name": "Graph builder step 7",
                "description": "Seventh step of the graph builder.",
            },
            {
                "name": "Graph builder step 8",
                "description": "Eighth step of the graph builder.",
            },
            {
                "name": "Graph builder step 9",
                "description": "Ninth step of the graph builder.",
            },
            {
                "name": "Graph builder step 10",
                "description": "Tenth step of the graph builder.",
            },
            {
                "name": "Graph builder step 11",
                "description": "Eleventh step of the graph builder.",
            },
        ]

        for step in steps:
            if self._session.query(TaskType).filter_by(name=step["name"]).first():
                continue
            task_type = TaskType(
                name=step["name"],
                description=step["description"],
            )
            self._session.add(task_type)

        # We populate an array with the task types.
        self._task_type_ids = [
            self._session.query(TaskType).filter_by(name=step["name"]).first().id
            for step in steps
        ]

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

        return (
            self._session.query(Task).filter_by(id=enrichable.task_id).first().status
            == "PENDING"
        )

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
        return (
            self._session.query(DataPayload)
            .join(Task, Task.id == DataPayload.task_id)
            .filter(Task.status == "PENDING")
            .all()
        )

    def _create_new_task(self, enrichable: DataPayload) -> Task:
        # In the case of the data payload, there is no need
        # to create a new entry in the task table, as there is
        # already one associated to the data payload.
        return self._session.query(Task).filter_by(id=enrichable.task_id).first()

    def _create_new_derived_task(self, task_id: int, task_number: int) -> Task:
        """Create a new derived task.

        Parameters
        ----------
        task_id
            id of the task to derive.
        task_number
            number of the task to derive.

        Returns
        -------
        derived_task
            derived task.

        """
        derived_task = Task(
            task_type_id=self._task_type_ids[task_number],
            user_id=self._enricher.id,
        )

        self._session.add(derived_task)
        self._session.flush()

        self._session.add(
            DerivedTask(
                parent_task_id=task_id,
                derived_task_id=derived_task.id,
            )
        )

        derived_task.start(session=self._session)

        return derived_task

    def _enrich(self, enrichable: DataPayload, task: Task) -> bool:
        """Enrich the metadata of a enrichable class.

        Parameters
        ----------
        enrichable
            enrichable class to enrich.
        """
        # We set the status of the task associated to the enrichable to STARTED.
        path = enrichable.get_unsafe_path()

        results = self._extractor.extract(path)[0]

        if not results["success"]:
            return False

        extraction_path = results["destination"]

        directory = os.path.dirname(extraction_path)

        # We execute the dirty pipeline, which is composed
        # by a sequence of python scripts with parameters.

        shutil.rmtree(self._output_path, ignore_errors=True)

        os.makedirs(self._output_path, exist_ok=True)

        # We create a new derived task for the first step of the dirty pipeline.

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=0,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}01_enpkg_data_organization/src/create_architecture.py",
                    "--source_path",
                    f"{directory}/ms_data/processed",
                    "--target_path",
                    self._output_path,
                    "--source_metadata_path",
                    f"{directory}/metadata",
                    "--sample_metadata_filename",
                    "dbgi_tropical_toydataset_metadata.tsv",
                    "--lcms_method_params_filename",
                    "dbgi_tropical_toydataset_lcms_params.txt",
                    "--lcms_processing_params_filename",
                    "dbgi_tropical_toydataset_mzmine_params.xml",
                    "--polarity",
                    "pos",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=1,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}01_enpkg_data_processing/src/add_massive_id.py",
                    "--massive_id",
                    "MSV000092400",
                    "-p",
                    self._output_path,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=2,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}02_enpkg_taxo_enhancer/src/taxo_info_fetcher.py",
                    "-p",
                    self._output_path,
                    "-f",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=3,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}03_enpkg_mn_isdb_isdb_taxo/src/nb_indifile.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=4,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}04_enpkg_sirius_canopus/src/sirius_canopus_by_file.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=5,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}05_enpkg_meta_analysis/src/chemo_info_fetcher.py",
                    "-p",
                    self._output_path,
                    "--sql_name",
                    # THIS IS HARDCODED IN THE STEP SIX!!!
                    "structures_metadata.db",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=6,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}05_enpkg_meta_analysis/src/memo_unaligned_repo.py",
                    "-p",
                    self._output_path,
                    "--ionization",
                    "pos",
                    "--output",
                    "memo_matrix",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=7,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/01_a_rdf_enpkg_metadata_indi.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=8,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/01_b_rdf_enpkgmodule_metadata_indi.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=9,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/02_a_rdf_features_indi.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=10,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/02_b_rdf_features_spec2vec_indi.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=11,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/03_rdf_csi_annotations_indi.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=12,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/04_rdf_canopus_indi.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/05_rdf_isdb_annotations_indi.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=13,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/06_rdf_individual_mn_indi.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=14,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/07_rdf_structures_metadata_indi.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=15,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/08_rdf_merger.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=16,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/09_rdf_exporter.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        derived_task = self._create_new_derived_task(
            task.id,
            task_number=17,
        )

        try:
            subprocess.run(
                [
                    "python",
                    f"./{self._root}06_enpkg_graph_builder/src/individual_processing/09_rdf_exporter.py",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as process_exception:
            derived_task.failure(session=self._session, reason=process_exception)
            raise process_exception

        derived_task.success(session=self._session)

        # We zip the output directory as a tar.gz file and we move it to the safe subdirectory.

        subprocess.run(
            [
                "tar",
                "-czvf",
                enrichable.get_safe_path(),
                self._output_path,
            ],
            check=True,
        )

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
        task_document = TaskRelatedDocument(
            task_id=task.id,
            document_id=document.id,
        )

        self._session.add(task_document)

        # We set the task associated to the enrichable to SUCCESS.
        task.success()

        # We commit the changes.

        # raise NotImplementedError("This method should be implemented in derived classes.")
        return True
