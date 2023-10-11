"""Test to ensure that the package does not suffer from circular imports."""
from emikg_interfaces import User


def test_imports_circularity():
    """Test to ensure that the package does not suffer from circular imports."""
    assert User
