"""Submodule providing database proxy classes that concretely implement the interfaces from enpkg_interfaces."""

from .user import User
from .translation import Translation

__all__ = ["User", "Translation"]