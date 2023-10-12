"""Module providing core models for the application."""
from alchemy_wrapper.models import Base
from alchemy_wrapper.database import engine, Session

Base.metadata.create_all(bind=engine)

__all__ = ["Base", "engine", "Session"]
