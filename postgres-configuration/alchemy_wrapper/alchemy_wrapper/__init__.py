"""Module providing core models for the application."""
from .models import Base
from .database import engine, Session

Base.metadata.create_all(bind=engine)

__all__ = ["Base", "engine", "Session"]
