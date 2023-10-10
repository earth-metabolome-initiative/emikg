"""Test to ensure that the package does not suffer from circular imports."""
from enpkg_interfaces import User


def test_imports_circularity():
    """Test to ensure that the package does not suffer from circular imports."""
    assert User
