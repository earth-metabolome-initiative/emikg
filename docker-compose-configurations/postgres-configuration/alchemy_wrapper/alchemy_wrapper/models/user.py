"""SQLAlchemy model for the user table."""

from sqlalchemy import Column, Integer, String, DateTime
from enpkg_interfaces import User as UserInterface
from enpkg_interfaces.from_identifier import IdentifierNotFound

from .base import Base
from .administrator import Administrator
from .moderator import Moderator
from alchemy_wrapper import Session


class User(Base, UserInterface):
    """Define the User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
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
