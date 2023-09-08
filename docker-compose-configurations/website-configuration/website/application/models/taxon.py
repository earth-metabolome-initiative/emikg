"""Concretely implements the proxy taxon interface using SQLAlchemy."""
from enpkg_interfaces import Taxon as TaxonInterface

from ..exceptions import APIException
from .user import User
from ..tables import TaxonsTable

class Taxon(TaxonInterface):
    """Class to represent a taxon."""

    @staticmethod
    def is_valid_taxon_id(taxon_id: int) -> bool:
        """Check if taxon ID exists.

        Parameters
        ----------
        taxon_id : int
            taxon ID.

        Returns
        -------
        bool
            True if taxon ID exists, False otherwise.

        Implementative details
        ----------------------
        The method looks up whether the taxon ID exists in taxon_id
        column of the taxons table.
        """
        return TaxonsTable.is_valid_taxon_id(taxon_id)
    
    @staticmethod
    def is_valid_taxon_name(taxon_name: str) -> bool:
        """Check if taxon name exists.

        Parameters
        ----------
        taxon_name : str
            taxon name.

        Returns
        -------
        bool
            True if taxon name exists, False otherwise.

        Implementative details
        ----------------------
        The method looks up whether the taxon name exists in taxon_name
        column of the taxons table.
        """
        return TaxonsTable.is_valid_taxon_name(taxon_name)
    
    def get_author_user_id(self) -> int:
        """Return the taxon's author user ID"""
        return TaxonsTable.get_author_user_id_from_taxon_id(self._taxon_id)
    
    def delete(self):
        """Delete a taxon.

        Raises
        ------
        NotLogged
            If the user is not logged in.
        Unauthorized
            If the user is not the taxon author.
            If the user is not a moderator.

        Implementative details
        ----------------------
        The method deletes the taxon with the provided ID from the
        taxons table. If the taxon ID does not exist, an API exception
        is raised.
        """
        # We create user object from the Flask session,
        # which implicitly checks also whether the user is logged in.
        user = User.from_flask_session()

        # We check whether the user is the author of the taxon.
        if not user.is_author_of_taxon(self):
            # If the user is not the author of the taxon,
            # we check whether the user is a moderator.
            # If the user is not a moderator, we raise an
            # unauthorized exception.
            User.must_be_moderator()

        # We delete the taxon from the database.
        TaxonsTable.delete_taxon(self._taxon_id)
    
    @staticmethod
    def create(taxon_name: str) -> int:
        """Create a taxon and return its ID.

        Parameters
        ----------
        taxon_name : str
            Name of the taxon.

        Raises
        ------
        APIException
            If the taxon with the provided name already exists.
        NotLogged
            If the user is not logged in.

        """
        user = User.from_flask_session()

        # We check whether the provided taxon name already exists.
        # If it does, we raise an API exception.
        if Taxon.is_valid_taxon_name(taxon_name):
            raise APIException(
                "Taxon with the provided name already exists.",
                status_code=409
            )
        
        # We insert the taxon into the database.
        return TaxonsTable.create_taxon_from_taxon_name(
            taxon_name=taxon_name,
            user_id=user.get_user_id()
        )