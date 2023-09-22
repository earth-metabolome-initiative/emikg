"""Submodule providing the proxy for the specters table in the database, using SQLAlchemy.

Implementative details
----------------------
The SQL creation statement for the specters table is the following:

```sql
-- Create the "specters" table to store sample information
CREATE TABLE specters (
    id SERIAL PRIMARY KEY,
    -- The name of the specter, which should be unique
    specter_name VARCHAR(255) NOT NULL,
    -- The sample id from which this specter was derived
    derived_from INT REFERENCES samples(id) ON DELETE CASCADE,
    -- The path to the MASCOT file
    path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    -- Add other specter-related fields as needed
    created_by INT REFERENCES users(id) ON DELETE CASCADE,
    updated_by INT REFERENCES users(id) ON DELETE CASCADE,
    -- We require for the specter name to be unique
    UNIQUE (specter_name)
);
```

"""
from typing import List, Optional
from .database import db

class SpectersTable(db.Model):
    """Proxy for the specters table in the database, using SQLAlchemy."""

    __tablename__ = 'specters'

    id = db.Column(db.Integer, primary_key=True)
    specter_name = db.Column(db.String(255), unique=True, nullable=False)
    derived_from = db.Column(db.Integer, db.ForeignKey('samples.id'))
    path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Specter #{self.id}>'
    
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
        """
        return SpectersTable.query.filter_by(id=specter_id).count() > 0
    
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
        """
        return SpectersTable.query.filter_by(specter_name=specter_name).count() > 0
    
    @staticmethod
    def is_valid_user_id(user_id: int) -> bool:
        """Check if user ID has created a specter.

        Parameters
        ----------
        user_id : int
            user ID.

        Returns
        -------
        bool
            True if user ID exists, False otherwise.
        """
        return SpectersTable.query.filter_by(created_by=user_id).count() > 0
    
    @staticmethod
    def get_author_user_id_from_specter_id(specter_id: int) -> int:
        """Return the author user ID of a specter.

        Parameters
        ----------
        specter_id : int
            specter ID.

        Returns
        -------
        int
            Author user ID.
        """
        return SpectersTable.query.filter_by(id=specter_id).first().user_id
    
    @staticmethod
    def _get_parent_sample_id_from_specter_id(specter_id: int) -> int:
        """Return the parent sample ID of a specter.

        Parameters
        ----------
        specter_id : int
            specter ID.

        Returns
        -------
        int
            Parent sample ID.
        """
        return SpectersTable.query.filter_by(id=specter_id).first().derived_from
    
    @staticmethod
    def delete_specter_from_specter_id(specter_id: int) -> None:
        """Delete specter from specter ID.

        Parameters
        ----------
        specter_id : int
            specter ID.
        """
        SpectersTable.query.filter_by(id=specter_id).delete()
        db.session.commit()

    @staticmethod
    def create_specter(specter_name: str, user_id: int, taxon_id: int, parent_specter_id: Optional[int] = None) -> int:
        """Create a new specter from a specter name.

        Parameters
        ----------
        specter_name : str
            specter name.
        user_id : int
            user ID.
        taxon_id : int
            taxon ID.
        parent_specter_id: Optional[int] = None
            parent specter ID.

        Returns
        -------
        int
            Specter ID.
        """
        
        # We open a transaction, and insert a new specter in the specters table.

        with db.session.begin_nested():
            # We insert a new specter in the specters table.
            specter = SpectersTable(specter_name=specter_name, created_by=user_id, taxon_id=taxon_id, derived_from=parent_specter_id)
            db.session.add(specter)
            db.session.flush()
            specter_id = specter.id

            # We commit the transaction.
            db.session.commit()

        return specter_id
    
    @staticmethod
    def get_last_n_modified_specters(number_of_specters: int) -> List[str]:
        """Return the last n specters modified.

        Parameters
        ----------
        number_of_specters : int
            Number of specters to return.

        Returns
        -------
        List[str]
            List of taxon names.
        """
        query = SpectersTable.query.order_by(SpectersTable.updated_at.desc()).limit(
            number_of_specters
        )
        return [mv for mv in query.all()]

    @staticmethod
    def get_last_n_specters_updated_by_user_id(
        number_of_specters: int, user_id: int
    ) -> List[str]:
        """Return the last n specters updated by a user.

        Parameters
        ----------
        number_of_specters : int
            Number of specters to return.
        user_id : int
            User ID.

        Returns
        -------
        List[str]
            List of taxon names.
        """
        query = (
            SpectersTable.query.filter_by(updated_by=user_id)
            .order_by(SpectersTable.updated_at.desc())
            .limit(number_of_specters)
        )
        return [mv for mv in query.all()]