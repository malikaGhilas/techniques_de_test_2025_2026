"""Tests for PointSet and Triangles binary serialization."""
def test_deserialize_empty_pointset():
    """Test deserialization of an empty PointSet."""
    from triangulator.utils import deserialize_pointset
    data = b"\x00\x00\x00\x00"  # 0 points
    result = deserialize_pointset(data)
    assert result == []

def test_deserialize_single_point():
    """Test deserialization of a PointSet with one point."""
    from triangulator.utils import deserialize_pointset
    # (1.0, 2.5) en float32 big-endian
    data = b"\x00\x00\x00\x01\x3f\x80\x00\x00\x40\x20\x00\x00"
    result = deserialize_pointset(data)
    assert result == [(1.0, 2.5)]

def test_deserialize_multiple_points():
    """Test deserialization of a PointSet with multiple points."""
    from triangulator.utils import deserialize_pointset
    # 2 points : (0.0, 0.0) et (-1.0, 1.5)
    data = b"\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\xbf\x80\x00\x00\x3f\xc0\x00\x00"
    result = deserialize_pointset(data)
    expected = [(0.0, 0.0), (-1.0, 1.5)]
    assert result == expected