"""SQLAlchemy model for ORCID data."""
from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class ORCID(Base):
    """Define the ORCID model."""

    __tablename__ = "orcid"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    orcid = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<ORCID({self.orcid!r})>"

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
        return ORCID.query.filter_by(orcid=orcid).first() is not None
    
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
        return ORCID.query.filter_by(orcid=orcid).first().user_id