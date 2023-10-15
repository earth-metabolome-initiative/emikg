"""SQLAlchemy model for the socials that we want to make available for users.

This table will contain the names and metadata associated to various socials that
admins can make available, by adding new rows for new socials.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from alchemy_wrapper.models.base import Base
from alchemy_wrapper.database import Session
from emikg_interfaces import FromIdentifier

class Social(Base, FromIdentifier):

    __tablename__ = "socials"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    url = Column(String(255), nullable=False, unique=True)
    icon_path = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    @staticmethod
    def from_id(identifier: int) -> "Social":
        """Return a social object from a social ID."""
        return Session().query(Social).filter(Social.id == identifier).first()
    
    def get_id(self) -> int:
        """Return the ID of the social."""
        return self.id