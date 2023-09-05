"""Concretely implements the proxy user interface using SQLAlchemy."""
from flask import session
from dict_hash import sha256
from enpkg_interfaces import User as UserInterface
from time import time
from ..app import db
from ..exceptions import NotLoggedIn, Unauthorized, APIException


class User(UserInterface):
    """Concrete implementation of the user interface using SQLAlchemy."""

    @staticmethod
    def from_flask_session() -> "User":
        """Return a user object from the Flask session."""
        return User(
            user_id=User.session_user_id()
        )
    
    @staticmethod
    def from_token(token: str) -> "User":
        """Return a user object from a token.
        
        Parameters
        ----------
        token : str
            Token.
        
        Raises
        ------
        NotLoggedIn
            If the token is not valid.
        """
        user_id = db.session.query(
            db.table("tokens").column("user_id")
        ).where(
            db.table("tokens").column("token") == token
        ).scalar()
        if user_id is None:
            raise Unauthorized()
        return User(
            user_id=user_id
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
    
    def create_token(self, token_name: str) -> str:
        """Creates and returns a token for the current user with the given name."""

        # We check whether there is already a token with the given name for the current user.
        # If there is, we raise an exception.
        if self.has_token(token_name):
            raise APIException("Token name already taken for the current user.")
        
        # We insert the token name in the database.
        # This insertion is done using SQLAlchemy, and as the token is
        # required to be unique, we expect the insertion to fail if the
        # token name is already taken. This should be extremely rare, as
        # the token is created using as salt ingredients the current time,
        # the user ID and the token name. Still, we check for this case.
        # When such a case happens, we recreate the token and try again.
        while True:
             # We create a token for the current user with the given name.
            token = sha256({
                "time": time(),
                "user_id": self.get_user_id(),
                "token_name": token_name
            })

            try:
                db.session.execute(
                    db.insert("tokens").values(
                        user_id=self.get_user_id(),
                        token_name=token_name,
                        token=token
                    )
                )
                break
            except Exception as exception:
                if "UNIQUE constraint failed" in str(exception):
                    continue
                raise exception
        
        # We return the token.
        return token
        
    def delete_token(self, token_name: str) -> None:
        """Delete a token for the current user with the given name.
        
        Parameters
        ----------
        token_name: str
            Name of the token to delete.

        Raises
        ------
        APIException
            If the token name is not taken for the current user.
        """
        # We check whether there is already a token with the given name for the current user.
        # If there is not, we raise an exception.
        if not self.has_token(token_name):
            raise APIException("Token name not taken for the current user.")

        db.session.execute(
            db.delete("tokens").where(
                db.and_(
                    db.table("tokens").column("user_id") == self.get_user_id(),
                    db.table("tokens").column("token_name") == token_name
                )
            )
        )

    def has_token(self, token_name: str) -> bool:
        """Return True if the user has a token with the given name.
        
        Parameters
        ----------
        token_name : str
            Token name.
        """
        return db.session.query(
            db.exists().where(
                db.and_(
                    db.table("tokens").column("user_id") == self.get_user_id(),
                    db.table("tokens").column("token_name") == token_name
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