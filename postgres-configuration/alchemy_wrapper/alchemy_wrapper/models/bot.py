"""SQLAlchemy model for the bot table."""

from sqlalchemy import Column, Integer, ForeignKey

from alchemy_wrapper.models.base import Base

class Bot(Base):
    """SQLAlchemy model for the bot table."""

    __tablename__ = "bots"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    def __repr__(self):
        """Return a string representation of the object."""
        return f"<Bot(id={self.id}, user_id={self.user_id})>"
