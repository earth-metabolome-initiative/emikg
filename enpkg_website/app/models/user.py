"""Concretely implements the proxy user interface using SQLAlchemy."""
from flask import session

from enpkg_interfaces import User as UserInterface

from ..app import db
from ..exceptions import NotLoggedIn, Unauthorized


class User(UserInterface):
    """Concrete implementation of the user interface using SQLAlchemy."""

    @staticmethod
    def from_flask_session() -> "User":
        """Return a user object from the Flask session."""
        return User(
            user_id=User.session_user_id()
        )
    
    @staticmethod
    def session_user_id() -> int:
        """Return a user id from the Flask session."""
        if "user_id" not in session:
            raise NotLoggedIn()
        return session.get("user_id")
    
    def is_session_user(self) -> bool:
        """Return whether the current user instance is the session user."""
        return self.get_user_id() == User.session_user_id()

    @staticmethod
    def must_be_administrator() -> None:
        """Raise ValueError if the user is not an administrator."""
        if not User.from_flask_session().is_administrator():
            raise Unauthorized()

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
    
    @staticmethod
    def must_be_moderator() -> None:
        """Raise ValueError if the user is not an moderator."""
        if not User.from_flask_session().is_moderator():
            raise Unauthorized()

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

    @classmethod
    def is_valid_user_id(cls, user_id: int) -> bool:
        """Return True if the user ID is valid.
        
        Parameters
        ----------
        user_id : int
            User ID.
        """
        return db.session.query(
            db.exists().where(
                db.and_(
                    db.table("users").column("id") == user_id
                )
            )
        ).scalar()

    def delete(self):
        """Delete the user.
        
        Raises
        ------
        Unauthorized
            If the user is not an administrator.
            If the user requesting the deletion is not the user being deleted.

        Implementative details
        ----------------------
        This method is implemented by deleting the user from the database, i.e.
        by deleting from the "users" table the row whose primary ID is equal
        to the ID of the current user instance.
        """
        # If the current user is NOT the session user, then
        if not self.is_session_user():
            # The current user session must be an administrator
            User.must_be_administrator()
        
        # If the current user is the session user, or is an administrator,
        # then delete the user from the database
        db.session.execute(
            db.delete("users").where(
                db.table("users").column("id") == self.get_user_id()
            )
        )