"""Tests for the Triangulator API endpoints."""
def test_app_exists():
    """Vérifie que l'application Flask est bien créée."""
    from triangulator.app import app
    assert app is not None