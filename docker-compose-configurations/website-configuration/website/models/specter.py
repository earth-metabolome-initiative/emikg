"""Concretely implements the proxy specter interface using SQLAlchemy."""

from typing import List, Optional
from enpkg_interfaces import Specter as SpecterInterface
from ..application import app
from .user import User
from .taxon import Taxon
from .sample import Sample
from ..exceptions import APIException
from ..tables import SpectersTable


class Specter(SpecterInterface):
    """Class to represent a specter."""

    @staticmethod
    def is_valid_specter_id(specter_id: int) -> bool:
        """Check if specter ID exists.

        Parameters
        ----------
        specter_id : int
            specter ID.

        Returns
        -------
        bool
            True if specter ID exists, False otherwise.

        Implementative details
        ----------------------
        The method looks up whether the specter ID exists in id
        column of the specters table.
        """
        return SpectersTable.is_valid_specter_id(specter_id)
    
    @staticmethod
    def is_valid_specter_name(specter_name: str) -> bool:
        """Check if specter name exists.

        Parameters
        ----------
        specter_name : str
            specter name.

        Returns
        -------
        bool
            True if specter name exists, False otherwise.

        Implementative details
        ----------------------
        The method looks up whether the specter name exists in specter_name
        column of the specters table.
        """
        return SpectersTable.is_valid_specter_name(specter_name)
    
    def get_author_user_id(self) -> int:
        """Return the specter's author user ID"""
        return SpectersTable.get_author_user_id_from_specter_id(self._specter_id)
    
    def _get_parent_sampler(self) -> "Specter":
        """Return the parent specter."""
        return Sample(SpectersTable.get_author_user_id_from_specter_id(self._specter_id))
    
    def get_child_specters(self) -> List["Specter"]:
        """Return the child specters."""
        return [
            Specter(child_specter_id) for child_specter_id in SpectersTable.get_child_specters_from_specter_id(self._specter_id)
        ]
    
    def is_derived_specter(self) -> bool:
        """Return True if specter is derived from another specter."""
        return SpectersTable.is_derived_specter_from_specter_id(self._specter_id)
    
    def delete(self):
        """Delete the specter.
        
        Raises
        ------
        NotLogged
            If the user is not logged in.
        Unauthorized
            If the user is not the author of the specter.
            If the user is not a moderator.
        """
        user = User.from_flask_session()

        if not user.is_author_of_specter(self):
            User.must_be_moderator()

        SpectersTable.delete_specter_from_specter_id(self._specter_id)

    @staticmethod
    def create(
        taxon_id: int,
        specter_name: str,
        parent_specter_id: Optional[int] = None
    ) -> int:
        """Create a specter.
        
        Parameters
        ----------
        taxon_id : int
            Taxon ID.
        specter_name : str
            Specter name.
        parent_specter_id : Optional[int]
            Parent specter ID.

        Returns
        -------
        int
            Specter ID.

        Raises
        ------
        APIException
            If the taxon ID does not exist.
            If the parent specter ID does not exist.
            If the specter name already exists.
        NotLogged
            If the user is not logged in.
        """
        user = User.from_flask_session()

        if not Taxon.is_valid_taxon_id(taxon_id):
            raise APIException(
                f"Taxon ID #{taxon_id} does not exist.",
                400
            )

        if parent_specter_id is not None:
            if not Specter.is_valid_specter_id(parent_specter_id):
                raise APIException(
                    f"Parent specter ID #{parent_specter_id} does not exist.",
                    400
                )

        if Specter.is_valid_specter_name(specter_name):
            raise APIException(
                f"Specter name '{specter_name}' already exists.",
                400
            )

        return SpectersTable.create_specter_from_specter_name(
            specter_name=specter_name,
            user_id=user.get_user_id(),
            taxon_id=taxon_id,
            parent_specter_id=parent_specter_id
        )
    
    @staticmethod
    def get_last_n_modified_specters(number_of_specters: int) -> List["Specter"]:
        """Return the last n specters modified.

        Parameters
        ----------
        number_of_specters: int
            Number of specters to return.

        Returns
        -------
        List[specter]
            List of specters.
        """
        return [
            Specter(specter.id) for specter in SpectersTable.get_last_n_modified_specters(number_of_specters)
        ]
    
app.jinja_env.globals.update(
    get_last_n_modified_specters=Specter.get_last_n_modified_specters
)
