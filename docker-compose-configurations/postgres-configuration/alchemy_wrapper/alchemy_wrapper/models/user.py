"""SQLAlchemy model for the user table."""

from sqlalchemy import Column, Integer, String, DateTime

from .base import Base
from .administrator import Administrator
from .moderator import Moderator


class User(Base):
    """Define the User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

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
