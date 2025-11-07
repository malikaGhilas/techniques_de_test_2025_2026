"""Tests pour les utilitaires de sérialisation."""

def test_serialize_pointset_exists():
    """Vérifie que la fonction serialize_pointset existe."""
    from triangulator.utils import serialize_pointset
    points = [(0.0, 0.0)]
    data = serialize_pointset(points)
    assert data is not None