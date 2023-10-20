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

    def get_author(self) -> User:
        """Return author user."""
        return User.from_id(self.user_id)
    
    def get_task(self) -> Task:
        """Return task."""
        return Task.from_id(self.task_id)
    
    @staticmethod
    def from_id(id: int) -> "DataPayload":
        """Return data payload from id."""
        data_payload = DataPayload.query.filter_by(id=id).first()
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
    def get_task_type() -> str:
        """Return task type."""
        return "Data payload processing"

    @staticmethod
    def get_task_type() -> TaskType:
        """Return task type id."""
        session = Session()
        task_type = session.query(TaskType).filter_by(name=DataPayload.get_task_type()).first()
        if task_type is None:
            # If the task type does not exist, we create it.
            task_type = TaskType(name=DataPayload.get_task_type())
            session.add(task_type)
            session.commit()
        return task_type

    @staticmethod
    def new_data_payload(user: Type[UserInterface]) -> "DataPayload":
        """Create a new data payload."""
        with Session() as session:
            task = Task(
                user_id=user.get_id(),
                task_type_id=DataPayload.get_task_type().id,
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