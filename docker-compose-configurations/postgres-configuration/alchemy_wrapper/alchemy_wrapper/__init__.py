"""Module providing core models for the application."""
from .core_models import Base
from .database import engine

Base.metadata.create_all(bind=engine)

__all__ = ["Base", "engine"]
