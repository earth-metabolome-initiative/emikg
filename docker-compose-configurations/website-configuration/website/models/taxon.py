"""Concrete implementation of Taxon for the website, integrating from alchemy the db and providing sectioned taxon."""

from .sectioned import Sectioned, Section
from enpkg_interfaces import Taxon as TaxonInterface
from alchemy_wrapper.models import Taxon as TaxonTable
from ..exceptions import Unauthorized
from .user import User


class Taxon(Section, Sectioned, TaxonInterface):
    def __init__(self, taxon: TaxonTable):
        """Initialize the taxon object from a taxon ID."""
        self._taxon = taxon

    @staticmethod
    def from_id(identifier: int) -> "Taxon":
        """Return a taxon object from a taxon ID."""
        return Taxon(TaxonTable.from_id(identifier))

    def get_author(self) -> User:
        """Return the author of the taxon."""
        return User(self._taxon.get_author())

    def get_description(self) -> str:
        """Return the description of the taxon."""
        return self._taxon.get_description()

    def get_name(self) -> str:
        """Return the name of the taxon."""
        return self._taxon.get_name()

    def delete(self):
        """Delete the taxon."""

        user = User.from_flask_session()

        # Either the user is the author of the taxon, or the user is an admin.
        if not user.is_administrator() and not user.is_author_of(self):
            raise Unauthorized()

        self._taxon.delete()
