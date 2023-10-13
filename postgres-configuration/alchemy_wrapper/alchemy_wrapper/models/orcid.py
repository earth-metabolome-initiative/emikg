"""SQLAlchemy model for ORCID data."""
from sqlalchemy import Column, Integer, String, ForeignKey
from alchemy_wrapper.models.base import Base
from alchemy_wrapper.models.core import User
from alchemy_wrapper.database import Session

class ORCID(Base):
    """Define the ORCID model."""

    __tablename__ = "orcid"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    orcid = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<ORCID({self.orcid!r})>"

    @staticmethod
    def from_orcid(orcid: str) -> "ORCID":
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
        return Session().query(ORCID).filter_by(orcid=orcid).first()
    
    @staticmethod
    def is_valid_orcid(orcid: str) -> bool:
        """Check if ORCID is valid.

        Parameters
        ----------
        orcid : str
            ORCID.

        Returns
        -------
        bool
            True if ORCID is valid, False otherwise.
        """
        return ORCID.from_orcid(orcid) is not None
    
    @staticmethod
    def get_user_from_orcid(orcid: str) -> User:
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
        orcid = ORCID.from_orcid(orcid)
        if orcid is None:
            raise ValueError(f"ORCID {orcid} does not exist.")
        return User.from_id(orcid.user_id)
    
    @staticmethod
    def get_or_insert_user_from_orcid(orcid: str) -> User:
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
        orcid = ORCID.from_orcid(orcid)
        if orcid is None:
            session = Session()
            user = User(
                first_name="John",
                last_name="Wick",
                email="john@wick.com",
            )
            session.add(user)
            orcid = ORCID(user_id=user.id, orcid=orcid)
            session.add(orcid)
            session.commit()
        else:
            user = User.from_id(orcid.user_id)
        return user