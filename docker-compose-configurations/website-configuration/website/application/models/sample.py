"""Concretely implements the proxy sample interface using SQLAlchemy."""

from typing import List, Optional
from enpkg_interfaces import Sample as SampleInterface
from .user import User
from .taxon import Taxon
from ..exceptions import APIException

from ..application import db

class Sample(SampleInterface):
    """Class to represent a sample."""

    @staticmethod
    def is_valid_sample_id(sample_id: int) -> bool:
        """Check if sample ID exists.

        Parameters
        ----------
        sample_id : int
            sample ID.

        Returns
        -------
        bool
            True if sample ID exists, False otherwise.

        Implementative details
        ----------------------
        The method looks up whether the sample ID exists in id
        column of the samples table.
        """
        return db.session.query(
            db.exists().where(
                db.and_(
                    db.table("samples").column("id") == sample_id
                )
            )
        ).scalar()
    
    @staticmethod
    def is_valid_sample_name(sample_name: str) -> bool:
        """Check if sample name exists.

        Parameters
        ----------
        sample_name : str
            sample name.

        Returns
        -------
        bool
            True if sample name exists, False otherwise.

        Implementative details
        ----------------------
        The method looks up whether the sample name exists in sample_name
        column of the samples table.
        """
        return db.session.query(
            db.exists().where(
                db.and_(
                    db.table("samples").column("sample_name") == sample_name
                )
            )
        ).scalar()
    
    def get_author_user_id(self) -> int:
        """Return the sample's author user ID"""
        return db.session.execute(
            """
            SELECT author_user_id
            FROM samples
            WHERE id = :sample_id
            """,
            sample_id= self.get_sample_id()
        ).scalar()
    
    def _get_parent_sample(self) -> "Sample":
        """Return the parent sample."""
        return Sample(db.session.execute(
            """
            SELECT parent_sample_id
            FROM samples
            WHERE id = :sample_id
            """,
            sample_id= self.get_sample_id()
        ).scalar())
    
    def get_child_samples(self) -> List["Sample"]:
        """Return the child samples."""
        return [
            Sample(child_sample_id) for child_sample_id in db.session.execute(
                """
                SELECT id
                FROM samples
                WHERE parent_sample_id = :sample_id
                """,
                sample_id= self.get_sample_id()
            ).fetchall()
        ]
    
    def is_derived_sample(self) -> bool:
        """Return True if sample is derived from another sample."""
        return db.session.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM samples
                WHERE parent_sample_id = :sample_id
            )
            """,
            sample_id=self.get_sample_id()
        ).scalar()
    
    def delete(self):
        """Delete the sample.
        
        Raises
        ------
        NotLogged
            If the user is not logged in.
        Unauthorized
            If the user is not the author of the sample.
            If the user is not a moderator.
        """
        user = User.from_flask_session()

        if not user.is_author_of_sample(self):
            User.must_be_moderator()

        db.session.execute(
            """
            DELETE FROM samples
            WHERE id = :sample_id
            """,
            sample_id= self.get_sample_id()
        )

    @staticmethod
    def create(
        taxon_id: int,
        sample_name: str,
        parent_sample_id: Optional[int] = None
    ) -> int:
        """Create a sample.
        
        Parameters
        ----------
        taxon_id : int
            Taxon ID.
        sample_name : str
            Sample name.
        parent_sample_id : Optional[int]
            Parent sample ID.

        Returns
        -------
        int
            Sample ID.

        Raises
        ------
        APIException
            If the taxon ID does not exist.
            If the parent sample ID does not exist.
            If the sample name already exists.
        NotLogged
            If the user is not logged in.
        """
        user = User.from_flask_session()

        if not Taxon.is_valid_taxon_id(taxon_id):
            raise APIException(
                f"Taxon ID #{taxon_id} does not exist.",
                400
            )

        if parent_sample_id is not None:
            if not Sample.is_valid_sample_id(parent_sample_id):
                raise APIException(
                    f"Parent sample ID #{parent_sample_id} does not exist.",
                    400
                )

        if Sample.is_valid_sample_name(sample_name):
            raise APIException(
                f"Sample name '{sample_name}' already exists.",
                400
            )

        sample_id = db.session.execute(
            """
            INSERT INTO samples (
                taxon_id,
                sample_name,
                parent_sample_id,
                author_user_id
            )
            VALUES (
                :taxon_id,
                :sample_name,
                :parent_sample_id,
                :author_user_id
            )
            RETURNING id
            """,
            {
                "taxon_id": taxon_id,
                "sample_name": sample_name,
                "parent_sample_id": parent_sample_id,
                "author_user_id": user.get_user_id()
            }
        ).scalar()

        return sample_id