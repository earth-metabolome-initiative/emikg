"""SQLAlchemy class for data_payload table.

A data payload is metadata associated with a file for the complete
batch pipeline processing enrichment. It is created from the website
APIs and is used to create a new batch job.
"""
from typing import Type
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from alchemy_wrapper.models.core import Base, User, Task, TaskType
from alchemy_wrapper.database import Session
from emikg_interfaces import IdentifierNotFound
from emikg_interfaces import User as UserInterface
from emikg_interfaces import Task as TaskInterface

class DataPayload(Base, TaskInterface):

    __tablename__ = "data_payloads"

    id = Column(Integer, primary_key=True)
    # The user who uploaded the file.
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    # The task associated with the payload.
    task_id = Column(Integer, ForeignKey(Task.id), nullable=False)
    # The time when the payload was created.
    created_at = Column(DateTime, nullable=False, default=func.now())

    def get_author(self, session: Type[Session]) -> User:
        """Return author user."""
        return User.from_id(self.user_id, session=session)
    
    def get_task(self, session: Type[Session]) -> Task:
        """Return task."""
        return Task.from_id(self.task_id, session=session)
    
    @staticmethod
    def from_id(id: int, session: Type[Session]) -> "DataPayload":
        """Return data payload from id."""
        data_payload = session.query(DataPayload).filter_by(id=id).first()
        if data_payload is None:
            raise IdentifierNotFound(f"Data payload with id {id} not found.")
        return data_payload
    
    def get_id(self) -> int:
        """Return id."""
        return self.id
    
    def get_payload_path(self) -> str:
        """Return payload path."""
        return f"/unsafe_data_payloads/{self.id}"

    @staticmethod
    def new_data_payload(
        user: Type[UserInterface],
        session: Type[Session],
    ) -> "DataPayload":
        """Create a new data payload."""
        task_type_name = "Data payload processing"
        task_type_description = "Task type for data payload processing."
        task_type = session.query(TaskType).filter_by(name=task_type_name).first()
        if task_type is None:
            # If the task type does not exist, we create it.
            task_type = TaskType(name=task_type_name, description=task_type_description)
            session.add(task_type)
            session.flush()
        task = Task(
            user_id=user.get_id(),
            task_type_id=task_type.id,
        )
        session.add(task)
        session.flush()
        data_payload = DataPayload(
            user_id=user.get_id(),
            task_id=task.id,
        )
        session.add(data_payload)
        session.commit()
        return data_payload