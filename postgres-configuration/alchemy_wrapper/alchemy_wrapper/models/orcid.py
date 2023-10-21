"""SQLAlchemy model for ORCID data."""
from typing import Type
from sqlalchemy import Column, Integer, String, ForeignKey
from alchemy_wrapper.models.base import Base
from alchemy_wrapper.models.core import User
from alchemy_wrapper.database import Session

class ORCID(Base):
    """Define the ORCID model."""

    __tablename__ = "orcid"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    orcid = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<ORCID({self.orcid!r})>"

    @staticmethod
    def from_orcid(orcid: str, session: Type[Session]) -> "ORCID":
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
        return session.query(ORCID).filter_by(orcid=orcid).first()
    
    @staticmethod
    def is_valid_orcid(orcid: str, session: Type[Session]) -> bool:
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
        return ORCID.from_orcid(orcid, session=session) is not None
    
    @staticmethod
    def get_user_from_orcid(orcid: str, session: Type[Session]) -> User:
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
        orcid = ORCID.from_orcid(orcid, session=session)
        if orcid is None:
            raise ValueError(f"ORCID {orcid} does not exist.")
        return User.from_id(orcid.user_id, session=session)
    
    @staticmethod
    def get_or_insert_user_from_orcid(orcid_code: str, session: Type[Session]) -> User:
        """Get user ID associated with the ORCID.

        Parameters
        ----------
        orcid_code : str
            ORCID.

        Returns
        -------
        int
            User ID associated with the ORCID.
        """
        orcid = ORCID.from_orcid(orcid_code, session=session)
        if orcid is None:
            user = User(
                first_name="John",
                last_name="Wick",
                email="john@wick.com",
            )
            session.add(user)
            session.flush()
            orcid = ORCID(user_id=user.id, orcid=orcid_code)
            session.add(orcid)
            session.commit()
        else:
            user = User.from_id(orcid.user_id, session=session)
        return user