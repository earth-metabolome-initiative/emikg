"""Concretely implements the proxy sample interface using SQLAlchemy."""

from typing import List, Optional
from enpkg_interfaces import Sample as SampleInterface
from ..application import app
from .user import User
from .taxon import Taxon
from ..exceptions import APIException


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
        return SamplesTable.is_valid_sample_id(sample_id)
    
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
        return SamplesTable.is_valid_sample_name(sample_name)
    
    def get_author_user_id(self) -> int:
        """Return the sample's author user ID"""
        return SamplesTable.get_author_user_id_from_sample_id(self._sample_id)
    
    def _get_parent_sample(self) -> "Sample":
        """Return the parent sample."""
        return Sample(SamplesTable.get_parent_sample_id_from_sample_id(self._sample_id))
    
    def get_child_samples(self) -> List["Sample"]:
        """Return the child samples."""
        return [
            Sample(child_sample_id) for child_sample_id in SamplesTable.get_child_samples_from_sample_id(self._sample_id)
        ]
    
    def is_derived_sample(self) -> bool:
        """Return True if sample is derived from another sample."""
        return SamplesTable.is_derived_sample_from_sample_id(self._sample_id)
    
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

        SamplesTable.delete_sample_from_sample_id(self._sample_id)

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

        return SamplesTable.create_sample_from_sample_name(
            sample_name=sample_name,
            user_id=user.get_user_id(),
            taxon_id=taxon_id,
            parent_sample_id=parent_sample_id
        )
    
    @staticmethod
    def get_last_n_modified_samples(number_of_samples: int) -> List["Sample"]:
        """Return the last n samples modified.

        Parameters
        ----------
        number_of_samples: int
            Number of samples to return.

        Returns
        -------
        List[sample]
            List of samples.
        """
        return [
            Sample(sample.id) for sample in SamplesTable.get_last_n_modified_samples(number_of_samples)
        ]
    
app.jinja_env.globals.update(
    get_last_n_modified_samples=Sample.get_last_n_modified_samples
)
