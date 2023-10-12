"""SQLAlchemy table for the access tokens."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from alchemy_wrapper.models.base import Base

class Token(Base):
    """Define the Token model."""

    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(512), nullable=False)
    created_at = Column(DateTime, nullable=False, default=DateTime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Token({self.jti!r})>"