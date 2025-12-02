"""Tests for triangulator services."""

def test_fetch_pointset_from_manager_returns_bytes():
    """Test that fetch_pointset_from_manager returns binary data."""
    from triangulator.services import fetch_pointset_from_manager
    result = fetch_pointset_from_manager("dummy_id")
    assert isinstance(result, bytes)
    assert len(result) > 0