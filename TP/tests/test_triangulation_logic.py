"""Tests for the core triangulation logic."""
def test_triangulate_function_exists():
    """Vérifie que la fonction triangulate existe."""
    from triangulator.services import triangulate
    assert triangulate is not None