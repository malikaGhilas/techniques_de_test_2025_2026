"""Tests for PointSet and Triangles binary serialization."""
def test_import_serialize_pointset():
    """Vérifie que la fonction serialize_pointset existe."""
    from triangulator.utils import serialize_pointset
    assert serialize_pointset is not None