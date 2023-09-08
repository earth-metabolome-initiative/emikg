"""Submodule providing the proxy for the ORCID table in the database, using SQLAlchemy.

Implementative details
----------------------
The SQL creation statement for the ORCID table is the following:

```sql
CREATE TABLE orcid (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    orcid VARCHAR(255) NOT NULL,
    -- Add other ORCID-related fields as needed
    -- The ORCID must be unique
    UNIQUE (orcid)
);
```

"""
from .database import db

class ORCIDTable(db.Model):
    """Proxy for the ORCID table in the database, using SQLAlchemy."""
    __tablename__ = 'orcid'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    orcid = db.Column(db.String(255), nullable=False, unique=True)
    # Add other ORCID-related fields as needed
    # The ORCID must be unique

    def __repr__(self):
        return f'<ORCIDTable {self.orcid}>'
    
    @staticmethod
    def is_valid_orcid(orcid: str) -> bool:
        """Check if ORCID exists.

        Parameters
        ----------
        orcid : str
            ORCID.

        Returns
        -------
        bool
            True if ORCID exists, False otherwise.
        """
        return ORCIDTable.query.filter_by(orcid=orcid).first() is not None
    
    @staticmethod
    def get_user_id_from_orcid(orcid: str) -> int:
        """Get user ID associated with the ORCID.

        Parameters
        ----------
        orcid : str
            ORCID.

        Returns
        -------
        int
            User ID associated with the ORCID.
        """
        return ORCIDTable.query.filter_by(orcid=orcid).first().user_id