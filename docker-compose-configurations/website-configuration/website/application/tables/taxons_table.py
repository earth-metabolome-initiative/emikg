"""Submodule providing the proxy for the taxons table in the database, using SQLAlchemy.

Implementative details
----------------------
The SQL creation statement for the taxons table is the following:

```sql
CREATE TABLE taxons (
    id SERIAL PRIMARY KEY,
    taxon_name VARCHAR(255) NOT NULL,
    taxon_description TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    -- Add other metadata fields as needed
    created_by INT REFERENCES users(id) ON DELETE CASCADE,
    updated_by INT REFERENCES users(id) ON DELETE CASCADE,
    -- The taxon name must be unique
    UNIQUE (taxon_name)
);
```

"""
from typing import List
import datetime
from .database import db


class TaxonsTable(db.Model):
    """Proxy for the taxons table in the database, using SQLAlchemy."""

    __tablename__ = "taxons"
    id = db.Column(db.Integer, primary_key=True)
    taxon_name = db.Column(db.String(255), unique=True, nullable=False)
    taxon_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow
    )
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Taxon #{self.id}>"

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
        """
        return TaxonsTable.query.filter_by(id=taxon_id).count() > 0
    
    @staticmethod
    def get_entry_from_taxon_id(taxon_id: int) -> "TaxonsTable":
        """Check if taxon ID exists.

        Parameters
        ----------
        taxon_id : int
            taxon ID.

        Returns
        -------
        bool
            True if taxon ID exists, False otherwise.
        """
        return TaxonsTable.query.filter_by(id=taxon_id).first()

    @staticmethod
    def get_last_n_modified_taxons(number_of_taxons: int) -> List[str]:
        """Return the last n taxons modified.

        Parameters
        ----------
        number_of_taxons : int
            Number of taxons to return.

        Returns
        -------
        List[str]
            List of taxon names.
        """
        query = TaxonsTable.query.order_by(TaxonsTable.updated_at.desc()).limit(
            number_of_taxons
        )
        return [mv for mv in query.all()]

    @staticmethod
    def get_last_n_taxons_updated_by_user_id(
        number_of_taxons: int, user_id: int
    ) -> List[str]:
        """Return the last n taxons updated by a user.

        Parameters
        ----------
        number_of_taxons : int
            Number of taxons to return.
        user_id : int
            User ID.

        Returns
        -------
        List[str]
            List of taxon names.
        """
        query = (
            TaxonsTable.query.filter_by(updated_by=user_id)
            .order_by(TaxonsTable.updated_at.desc())
            .limit(number_of_taxons)
        )
        return [mv for mv in query.all()]

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
        """
        return TaxonsTable.query.filter_by(taxon_name=taxon_name).count() > 0

    @staticmethod
    def create_taxon(taxon_name: str, description: str, user_id: int) -> int:
        """Create a new taxon from a taxon name.

        Parameters
        ----------
        taxon_name : str
            taxon name.
        description : str
            taxon description.
        user_id : int
            user ID.

        Returns
        -------
        int
            Taxon ID.
        """

        # We open a transaction, and insert a new taxon in the taxons table.

        with db.session.begin_nested():
            # We insert a new taxon in the taxons table.
            taxon = TaxonsTable(
                taxon_name=taxon_name,
                taxon_description=description,
                created_by=user_id,
                updated_by=user_id,
            )
            db.session.add(taxon)
            db.session.flush()
            taxon_id = taxon.id

            # We commit the transaction.
            db.session.commit()

        return taxon_id

    @staticmethod
    def get_author_user_id_from_taxon_id(taxon_id: int) -> int:
        """Return the taxon's author user ID

        Parameters
        ----------
        taxon_id : int
            Taxon ID.

        Returns
        -------
        int
            User ID.
        """
        return db.session.execute(
            """
            SELECT user_id FROM taxons
            WHERE id = :taxon_id
            """,
            taxon_id=taxon_id,
        ).scalar()

    @staticmethod
    def delete_taxon(taxon_id: int) -> None:
        """Delete a taxon.

        Parameters
        ----------
        taxon_id : int
            taxon ID.
        """

        # We open a transaction, and delete the taxon from the taxons table.
        # We commit the transaction.
        taxon = TaxonsTable.query.filter_by(id=taxon_id).first()
        db.session.delete(taxon)
        db.session.commit()

    @staticmethod
    def find_taxons_like(needle: str) -> List["TaxonsTable"]:
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
        query = TaxonsTable.query.filter(
            TaxonsTable.taxon_name.ilike(f"%{needle}%")
        ).limit(10)
        return [mv for mv in query.all()]
