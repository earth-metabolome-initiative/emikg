"""SQLAlchemy model for moderator table."""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from alchemy_wrapper.models.base import Base


class Moderator(Base):
    
    __tablename__ = "moderators"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", unique=True, ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="moderator")

    def __repr__(self):
        return f"<Moderator(id={self.id}, user_id={self.user_id})>"
