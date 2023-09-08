"""Submodule providing the proxy for the moderators table in the database, using SQLAlchemy.

Implementative details
----------------------
The SQL creation statement for the moderators table is the following:

```sql
CREATE TABLE moderators (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    -- Add other moderator-related fields as needed
    -- The user_id must be unique
    UNIQUE (user_id)
);
```

"""

from .database import db

class ModeratorsTable(db.Model):
    """Proxy for the moderators table in the database, using SQLAlchemy."""

    __tablename__ = 'moderators'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    def __repr__(self):
        return f'<Moderator #{self.id}>'
    
    @staticmethod
    def is_valid_moderator_id(moderator_id: int) -> bool:
        """Check if moderator ID exists.

        Parameters
        ----------
        moderator_id : int
            moderator ID.

        Returns
        -------
        bool
            True if moderator ID exists, False otherwise.
        """
        return ModeratorsTable.query.filter_by(id=moderator_id).count() > 0
    
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
        return ModeratorsTable.query.filter_by(user_id=user_id).count() > 0
    
    @staticmethod
    def create_moderator_from_user_id(user_id: int) -> int:
        """Create a new moderator from a user ID.

        Parameters
        ----------
        user_id : int
            user ID.

        Returns
        -------
        int
            Moderator ID.
        """
        
        moderator = ModeratorsTable(user_id=user_id)
        db.session.add(moderator)
        db.session.commit()
        return moderator.id
    
    @staticmethod
    def delete_moderator(moderator_id: int) -> None:
        """Delete a moderator.

        Parameters
        ----------
        moderator_id : int
            moderator ID.
        """
        
        moderator = ModeratorsTable.query.filter_by(id=moderator_id).first()
        db.session.delete(moderator)
        db.session.commit()

    @staticmethod
    def delete_moderator_from_user_id(user_id: int) -> None:
        """Delete a moderator.

        Parameters
        ----------
        user_id : int
            user ID.
        """
        
        moderator = ModeratorsTable.query.filter_by(user_id=user_id).first()
        db.session.delete(moderator)
        db.session.commit()