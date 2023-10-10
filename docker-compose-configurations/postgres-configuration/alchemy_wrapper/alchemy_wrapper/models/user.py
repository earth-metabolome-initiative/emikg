"""SQLAlchemy model for the user table."""

from typing import List
from alchemy_wrapper import Session
from sqlalchemy import Column, DateTime, Integer, String

from enpkg_interfaces import User as UserInterface
from enpkg_interfaces.from_identifier import IdentifierNotFound

from .administrator import Administrator
from .base import Base
from .spectra_collection import SpectraCollection
from .sample import Sample
from .moderator import Moderator


class User(Base, UserInterface):
    """Define the User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    @staticmethod
    def from_id(identifier: int) -> "User":
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
        user = User.query.filter_by(id=identifier).first()
        if user is None:
            raise IdentifierNotFound(f"User with id {identifier} not found")
        return user

    def get_id(self) -> int:
        """Return the identifier of the user."""
        return self.id

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"

    def is_moderator(self):
        """Check if user is a moderator.

        Implementation details
        ----------------------
        This method checks if the user is a moderator by checking if the user
        id appears in the moderators table.
        """
        # We query the moderators table to check if the user is a moderator
        return Moderator.query.filter_by(user_id=self.id).first() is not None

    def is_administrator(self):
        """Check if user is an administrator.

        Implementation details
        ----------------------
        This method checks if the user is an administrator by checking if the user
        id appears in the administrators table.
        """
        # We query the administrators table to check if the user is an administrator
        return Administrator.query.filter_by(user_id=self.id).first() is not None

    def delete(self):
        """Delete the user."""
        # We delete the user from the database
        session = Session()
        session.delete(self)
        session.commit()

    def get_spectra_collections(
        self, number_of_records: int
    ) -> List[SpectraCollection]:
        """Return list of spectra collections created by the user.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        # We return the most recent spectra collections created by the user
        return (
            SpectraCollection.query.filter_by(user_id=self.id)
            .order_by(SpectraCollection.updated_at.desc())
            .limit(number_of_records)
            .all()
        )

    def get_samples(self, number_of_records: int) -> List[Sample]:
        """Return list of samples created by the user.

        Parameters
        ----------
        number_of_records : int
            Maximum number of records to return.
        """
        # We return the most recent samples created by the user
        return (
            Sample.query.filter_by(user_id=self.id)
            .order_by(Sample.updated_at.desc())
            .limit(number_of_records)
            .all()
        )