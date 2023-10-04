"""SQLAlchemy database proxy relative to the open tree of life table."""
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OpenTreeOfLifeEntry(Base):
    """Define the OpenTreeOfLifeEntry model."""

    __tablename__ = "open_tree_of_life"

    id = Column(Integer, primary_key=True)
    ott_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<OpenTreeOfLifeEntry({self.ott_id!r})>"
