"""Concretely implements the proxy taxon interface using SQLAlchemy."""
from enpkg_interfaces import Taxon as TaxonInterface

from ..application import db
from ..exceptions import APIException
from .user import User

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
        return db.session.query(
            db.exists().where(
                db.and_(
                    db.table("taxons").column("id") == taxon_id
                )
            )
        ).scalar()
    
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
        return db.session.query(
            db.exists().where(
                db.and_(
                    db.table("taxons").column("taxon_name") == taxon_name
                )
            )
        ).scalar()
    
    def get_author_user_id(self) -> int:
        """Return the taxon's author user ID"""
        return db.session.execute(
            """
            SELECT created_by FROM taxons
            WHERE id = :taxon_id
            """,
            taxon_id=self._taxon_id
        ).scalar()
    
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
        db.engine.execute(
            """
            DELETE FROM taxons
            WHERE id = :taxon_id
            """,
            taxon_id=self._taxon_id
        )
    
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
        db.engine.execute(
            """
            INSERT INTO taxons (taxon_name, created_by)
            VALUES (:taxon_name, :user_id)
            """,
            taxon_name=taxon_name,
            user_id=user.get_user_id()
        )

        # We retrieve the ID of the newly created taxon.
        taxon_id = db.session.execute(
            """
            SELECT id FROM taxons
            WHERE taxon_name = :taxon_name
            """,
            taxon_name=taxon_name
        ).scalar()

        return taxon_id