"""Submodule providing the proxy for the samples table in the database, using SQLAlchemy.

Implementative details
----------------------
The SQL creation statement for the samples table is the following:

```sql
-- Create the "samples" table to store sample information
CREATE TABLE samples (
    id SERIAL PRIMARY KEY,
    -- The name of the sample, which should be unique
    sample_name VARCHAR(255) NOT NULL,
    -- Some samples are derived from other samples,
    -- except for the first sample, which is not
    -- derived from any other sample. This means
    -- that the "derived_from" column can be NULL.
    derived_from INT REFERENCES samples(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    -- Add other sample-related fields as needed
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    taxon_id INT REFERENCES taxons(id) ON DELETE CASCADE,
    -- We require for the sample name to be unique
    UNIQUE (sample_name)
);
```

"""
from typing import List, Optional
from .database import db

class SamplesTable(db.Model):
    """Proxy for the samples table in the database, using SQLAlchemy."""

    __tablename__ = 'samples'

    id = db.Column(db.Integer, primary_key=True)
    sample_name = db.Column(db.String(255), unique=True, nullable=False)
    derived_from = db.Column(db.Integer, db.ForeignKey('samples.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    taxon_id = db.Column(db.Integer, db.ForeignKey('taxons.id'), nullable=False)

    def __repr__(self):
        return f'<Sample #{self.id}>'
    
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
        """
        return SamplesTable.query.filter_by(id=sample_id).count() > 0
    
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
        """
        return SamplesTable.query.filter_by(sample_name=sample_name).count() > 0
    
    @staticmethod
    def is_valid_user_id(user_id: int) -> bool:
        """Check if user ID exists.

        Parameters
        ----------
        user_id : int
            user ID.

        Returns
        -------
        bool
            True if user ID exists, False otherwise.
        """
        return SamplesTable.query.filter_by(user_id=user_id).count() > 0
    
    @staticmethod
    def get_author_user_id_from_sample_id(sample_id: int) -> int:
        """Return the author user ID of a sample.

        Parameters
        ----------
        sample_id : int
            sample ID.

        Returns
        -------
        int
            Author user ID.
        """
        return SamplesTable.query.filter_by(id=sample_id).first().user_id
    
    @staticmethod
    def _get_parent_sample_id_from_sample_id(sample_id: int) -> int:
        """Return the parent sample ID of a sample.

        Parameters
        ----------
        sample_id : int
            sample ID.

        Returns
        -------
        int
            Parent sample ID.
        """
        return SamplesTable.query.filter_by(id=sample_id).first().derived_from
    
    @staticmethod
    def get_child_samples_from_sample_id(sample_id: int) -> List[int]:
        """Return the child sample IDs of a sample.

        Parameters
        ----------
        sample_id : int
            sample ID.

        Returns
        -------
        List[int]
            Child sample IDs.
        """
        return [
            child_sample.id for child_sample in SamplesTable.query.filter_by(derived_from=sample_id).all()
        ]
    
    @staticmethod
    def is_derived_sample_from_sample_id(sample_id: int) -> bool:
        """Return True if sample is derived from another sample.

        Parameters
        ----------
        sample_id : int
            sample ID.

        Returns
        -------
        bool
            True if sample is derived from another sample, False otherwise.
        """
        return SamplesTable.query.filter_by(id=sample_id).first().derived_from is not None
    
    @staticmethod
    def delete_sample_from_sample_id(sample_id: int) -> None:
        """Delete sample from sample ID.

        Parameters
        ----------
        sample_id : int
            sample ID.
        """
        SamplesTable.query.filter_by(id=sample_id).delete()
        db.session.commit()

    @staticmethod
    def create_sample_from_sample_name(sample_name: str, user_id: int, taxon_id: int, parent_sample_id: Optional[int] = None) -> int:
        """Create a new sample from a sample name.

        Parameters
        ----------
        sample_name : str
            sample name.
        user_id : int
            user ID.
        taxon_id : int
            taxon ID.
        parent_sample_id: Optional[int] = None
            parent sample ID.

        Returns
        -------
        int
            Sample ID.
        """
        
        # We open a transaction, and insert a new sample in the samples table.

        with db.session.begin_nested():
            # We insert a new sample in the samples table.
            sample = SamplesTable(sample_name=sample_name, user_id=user_id, taxon_id=taxon_id, derived_from=parent_sample_id)
            db.session.add(sample)
            db.session.flush()
            sample_id = sample.id

            # We commit the transaction.
            db.session.commit()

        return sample_id