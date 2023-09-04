"""Concretely implements the proxy user interface using SQLAlchemy."""
from flask import session

from enpkg_interfaces import User as UserInterface

from ..app import db


class User(UserInterface):
    """Concrete implementation of the user interface using SQLAlchemy."""

    @staticmethod
    def from_flask_session() -> "User":
        """Return a user object from the Flask session."""
        return User(
            user_id=session.get("user_id")
        )

    def is_administrator(self) -> bool:
        """Return True if the user is an administrator.
        
        Implementative details
        ----------------------
        This method is implemented by looking up whether the user id
        exists within the "administrators" table in the database.
        The "administrators" table is composed of two columns, one
        is the primary ID of the administrators table, and the latter is
        the user ID itself.
        """
        return db.session.query(
            db.exists().where(
                db.and_(
                    db.table("administrators").column("user_id") == self.get_user_id()
                )
            )
        ).scalar()
    
    def is_moderator(self) -> bool:
        """Return True if the user is a moderator.
        
        Implementative details
        ----------------------
        This method is implemented by looking up whether the user id
        exists within the "moderators" table in the database.
        The "moderators" table is composed of two columns, one
        is the primary ID of the moderators table, and the latter is
        the user ID itself.
        """
        return db.session.query(
            db.exists().where(
                db.and_(
                    db.table("moderators").column("user_id") == self.get_user_id()
                )
            )
        ).scalar()