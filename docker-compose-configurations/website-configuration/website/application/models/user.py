"""Concretely implements the proxy user interface using SQLAlchemy."""
from flask import session

from enpkg_interfaces import User as UserInterface

from ..exceptions import APIException, NotLoggedIn, Unauthorized
from ..tables import ORCIDTable, ModeratorsTable, AdministratorsTable, UsersTable, TokensTable


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
        # To execute this operation, the user must not be already logged in.
        if User.is_authenticated():
            raise APIException("User is already logged in.")
        user_id = TokensTable.get_user_id_from_token(token)
        if user_id is None:
            raise Unauthorized()
        
        # We add the user ID to the Flask session.
        session["user_id"] = user_id

        return User(
            user_id=user_id
        )
    
    @staticmethod
    def from_orcid(orcid: str) -> "User":
        """Return a user object from an ORCID.
        
        Parameters
        ----------
        orcid : str
            ORCID.
        
        Implementation details
        ----------------------
        The method looks up whether the ORCID exists in the orcid
        table of the database. If it does, we create a new user object
        from the user ID associated with the ORCID. If it does not, then
        we are currently creating a new user. We insert a new user in the
        users table, and return a new user object from the user ID of the
        newly inserted user. In the same transaction, we also insert the
        ORCID in the orcid table alongside the user ID. The transactional
        aspect is important, as it ensures that the ORCID is inserted only
        if the user is successfully inserted.
        Finally, we return a new user object from the user ID of the newly
        inserted user.
        """
        # To execute this operation, the user must not be already logged in.
        if User.is_authenticated():
            raise APIException("User is already logged in.")

        # We look up whether the ORCID exists in the orcid table of the database.
        # If it does, we create a new user object from the user ID associated with
        # the ORCID.
        user_id = ORCIDTable.get_user_id_from_orcid(orcid)

        if user_id is None:
            # Otherwise, we are currently creating a new user.
            # We open a transaction, and insert a new user in the users table.
            # We also insert the ORCID in the orcid table alongside the user ID.
            UsersTable.create_user_from_orcid(orcid)

        # We add the user ID to the Flask session.
        session["user_id"] = user_id

        # Finally, we return a new user object from the user ID of the newly
        # inserted user.
        return User(
            user_id=user_id
        )
    
    @staticmethod
    def logout() -> None:
        """Logout the user.
        
        Implementation details
        ----------------------
        The method removes the user ID from the Flask session.
        """
        session.pop("user_id", None)

    @staticmethod
    def is_authenticated() -> bool:
        """Return whether the user is authenticated."""
        return "user_id" in session
    
    @staticmethod
    def session_user_id() -> int:
        """Return a user id from the Flask session."""
        if not User.is_authenticated():
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
        return AdministratorsTable.is_valid_user_id(self.get_user_id())
    
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
        return ModeratorsTable.is_valid_user_id(self.get_user_id())

    @classmethod
    def is_valid_user_id(cls, user_id: int) -> bool:
        """Return True if the user ID is valid.
        
        Parameters
        ----------
        user_id : int
            User ID.
        """
        return UsersTable.is_valid_user_id(user_id)
    
    def create_token(self, token_name: str) -> str:
        """Creates and returns a token for the current user with the given name."""

        # We check whether there is already a token with the given name for the current user.
        # If there is, we raise an exception.
        if self.has_token(token_name):
            raise APIException("Token name already taken for the current user.")
        
        return TokensTable.create_token(
            user_id=self.get_user_id(),
            token_name=token_name
        )
        
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

        TokensTable.delete_token_from_token_name_and_user_id(
            user_id=self.get_user_id(),
            token_name=token_name
        )
        

    def has_token(self, token_name: str) -> bool:
        """Return True if the user has a token with the given name.
        
        Parameters
        ----------
        token_name : str
            Token name.
        """
        return TokensTable.has_token_from_token_name_and_user_id(
            user_id=self.get_user_id(),
            token_name=token_name
        )

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
        UsersTable.delete_user(self.get_user_id())

    def promote_admin(self):
        """Promote the user to administrator.
        
        Raises
        ------
        Unauthorized
            If the user is not an administrator.

        Implementative details
        ----------------------
        This method is implemented by inserting the user ID in the "administrators"
        table, which is the table that contains the user IDs of the administrators.
        """
        # The current user session must be an administrator
        User.must_be_administrator()

        # If the current user is already an administrator, then we raise an exception
        if self.is_administrator():
            raise APIException("User is already an administrator.")
        
        # If the current user is the session user, or is an administrator,
        # then promote the user to administrator
        AdministratorsTable.create_administrator_from_user_id(self.get_user_id())

    def demote_admin(self):
        """Demote the user from administrator.
        
        Raises
        ------
        Unauthorized
            If the user is not an administrator.

        Implementative details
        ----------------------
        This method is implemented by deleting the user ID from the "administrators"
        table, which is the table that contains the user IDs of the administrators.
        """
        # The current user session must be an administrator
        User.must_be_administrator()

        # If the current user is NOT an administrator, then we raise an exception
        if not self.is_administrator():
            raise APIException("User is not an administrator.")
        
        # If the current user is the session user, or is an administrator,
        # then demote the user from administrator
        AdministratorsTable.delete_administrator_from_user_id(self.get_user_id())

    def promote_moderator(self):
        """Promote the user to moderator.
        
        Raises
        ------
        Unauthorized
            If the user is not an administrator.

        Implementative details
        ----------------------
        This method is implemented by inserting the user ID in the "moderators"
        table, which is the table that contains the user IDs of the moderators.
        """
        # The current user session must be an administrator
        User.must_be_administrator()

        # If the current user is already a moderator, then we raise an exception
        if self.is_moderator():
            raise APIException("User is already a moderator.")
        
        # If the current user is the session user, or is an administrator,
        # then promote the user to moderator
        ModeratorsTable.create_moderator_from_user_id(self.get_user_id())

    def demote_moderator(self):
        """Demote the user from moderator.
        
        Raises
        ------
        Unauthorized
            If the user is not an administrator.

        Implementative details
        ----------------------
        This method is implemented by deleting the user ID from the "moderators"
        table, which is the table that contains the user IDs of the moderators.
        """
        # The current user session must be an administrator
        User.must_be_administrator()

        # If the current user is NOT a moderator, then we raise an exception
        if not self.is_moderator():
            raise APIException("User is not a moderator.")
        
        # If the current user is the session user, or is an administrator,
        # then demote the user from moderator
        ModeratorsTable.delete_moderator_from_user_id(self.get_user_id())

    def illegal_user_id_callback(self, illegal_user_id: int) -> None:
        """Method called upon detection of an illegal user ID.
        
        Implementative details
        ----------------------
        This method handles the corner case where the provided user ID
        is not present in the database, but is equal to the ID of the
        current session. Such cases could represent users that have
        recently been banned or deleted, and that are still logged in.
        In such cases, we delete the session.
        """
        if illegal_user_id == session.get("user_id", None):
            User.logout()