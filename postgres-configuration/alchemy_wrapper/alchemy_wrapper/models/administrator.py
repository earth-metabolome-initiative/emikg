"""SQLAlchemy model for the administrator table.

Implementative details
----------------------
The administrator table is a two-column table that stores the users that are
also administrators of the application. The table is used to check whether a
user is an administrator or not. The table has the foreign key constraint
ON DELETE CASCADE, which means that if a user is deleted, the corresponding
administrator entry is also deleted.
"""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from alchemy_wrapper.models.base import Base


class Administrator(Base):
    __tablename__ = "administrators"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", unique=True, ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="administrator")

    def __repr__(self):
        return f"<Administrator(id={self.id}, user_id={self.user_id})>"
