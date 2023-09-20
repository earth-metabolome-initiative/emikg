"""Concretely implements the proxy taxon interface using SQLAlchemy."""
from enpkg_interfaces import Taxon as TaxonInterface
from typing import List
from ...application import app
from ..exceptions import APIException
from .user import User
from .translation import Translation
from ..tables import TaxonsTable


class Taxon(TaxonInterface):
    """Class to represent a taxon."""

    def __init__(self, taxon_id: int) -> None:
        """Initialize taxon object.

        Parameters
        ----------
        taxon_id : int
            taxon ID.

        Raises
        ------
        ValueError
            If the taxon ID does not exist.
        """
        if not self.is_valid_taxon_id(taxon_id):
            raise ValueError(f"Taxon ID #{taxon_id} does not exist.")

        self._entry = TaxonsTable.get_entry_from_taxon_id(taxon_id)

        super().__init__(taxon_id)

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
        return self._entry.created_by

    def get_taxon_name(self) -> str:
        """Return taxon name."""
        return self._entry.taxon_name
    
    def get_taxon_id(self) -> int:
        """Return taxon ID."""
        return self._entry.id
    
    def get_taxon_description(self) -> str:
        """Return taxon description."""
        return self._entry.taxon_description

    def get_taxon_url(self) -> str:
        """Return taxon URL."""
        return f"/{Translation.get_current_language()}/taxons/{self._entry.id}"

    @staticmethod
    def get_last_n_modified_taxons(number_of_taxons: int) -> List["Taxon"]:
        """Return the last n taxons modified.

        Parameters
        ----------
        number_of_taxons : int
            Number of taxons to return.

        Returns
        -------
        List[Taxon]
            List of taxons.
        """
        return [
            taxon for taxon in TaxonsTable.get_last_n_modified_taxons(number_of_taxons)
        ]

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
    def find_taxons_like(needle: str) -> List["Taxon"]:
        """Find taxons like a needle.

        Parameters
        ----------
        needle : str
            Needle.

        Returns
        -------
        List[str]
            List of taxon names.
        """
        return [
            Taxon(taxon.id)
            for taxon in TaxonsTable.find_taxons_like(needle)
        ]

    @staticmethod
    def create(taxon_name: str, description: str) -> "Taxon":
        """Create a taxon and return its ID.

        Parameters
        ----------
        taxon_name : str
            Name of the taxon.
        description : str
            Description of the taxon.

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
            )

        # We insert the taxon into the database.
        return Taxon(
            TaxonsTable.create_taxon(
                taxon_name=taxon_name,
                description=description,
                user_id=user.get_user_id()
            )
        )


app.jinja_env.globals.update(
    get_last_n_modified_taxons=Taxon.get_last_n_modified_taxons
)
