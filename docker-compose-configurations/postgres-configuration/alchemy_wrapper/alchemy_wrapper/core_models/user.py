"""SQLAlchemy model for the user table."""

from sqlalchemy import Column, Integer, String, DateTime

from .base import Base

class User(Base):
    """Define the User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"