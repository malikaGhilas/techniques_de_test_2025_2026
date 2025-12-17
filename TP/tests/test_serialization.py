"""Tests for PointSet and Triangles binary serialization."""

import pytest
from triangulator.utils import (
    deserialize_pointset,
    serialize_pointset,
    serialize_triangles,
)

# ==================== Tests de désérialisation PointSet ====================

def test_deserialize_empty_pointset():
    """Test deserialization of an empty PointSet."""
    data = b"\x00\x00\x00\x00"  # 0 points
    result = deserialize_pointset(data)
    assert result == []


def test_deserialize_single_point():
    """Test deserialization of a PointSet with one point."""
    # (1.0, 2.5) en float32 big-endian
    data = b"\x00\x00\x00\x01\x3f\x80\x00\x00\x40\x20\x00\x00"
    result = deserialize_pointset(data)
    assert len(result) == 1
    assert result[0][0] == pytest.approx(1.0)
    assert result[0][1] == pytest.approx(2.5)


def test_deserialize_multiple_points():
    """Test deserialization of a PointSet with multiple points."""
    # 2 points : (0.0, 0.0) et (-1.0, 1.5)
    data = (
        b"\x00\x00\x00\x02"  # 2 points
        b"\x00\x00\x00\x00\x00\x00\x00\x00"  # (0.0, 0.0)
        b"\xbf\x80\x00\x00\x3f\xc0\x00\x00"  # (-1.0, 1.5)
    )
    result = deserialize_pointset(data)
    expected = [(0.0, 0.0), (-1.0, 1.5)]
    assert len(result) == 2
    assert result[0][0] == pytest.approx(expected[0][0])
    assert result[0][1] == pytest.approx(expected[0][1])
    assert result[1][0] == pytest.approx(expected[1][0])
    assert result[1][1] == pytest.approx(expected[1][1])


# ==================== Tests de sérialisation PointSet ====================

def test_serialize_empty_pointset():
    """Test serialization of an empty PointSet."""
    points = []
    data = serialize_pointset(points)
    assert data == b"\x00\x00\x00\x00"


def test_serialize_single_point():
    """Test serialization of a single point."""
    points = [(1.0, 2.0)]
    data = serialize_pointset(points)
    assert len(data) == 4 + 8  # 4 (count) + 8 (point)
    num_points = int.from_bytes(data[:4], byteorder="big")
    assert num_points == 1


def test_serialize_multiple_points():
    """Test serialization of multiple points."""
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    data = serialize_pointset(points)
    expected_length = 4 + 8 * 3
    assert len(data) == expected_length
    num_points = int.from_bytes(data[:4], byteorder="big")
    assert num_points == 3


# ==================== Tests de réversibilité ====================

def test_serialize_deserialize_roundtrip():
    """Test that serialize→deserialize gives back original data."""
    original = [(0.0, 0.0), (1.5, 2.5), (-3.0, 4.0)]
    serialized = serialize_pointset(original)
    deserialized = deserialize_pointset(serialized)
    
    assert len(deserialized) == len(original)
    for i, (x, y) in enumerate(original):
        assert deserialized[i][0] == pytest.approx(x)
        assert deserialized[i][1] == pytest.approx(y)


# ==================== Tests de valeurs extrêmes ====================

def test_deserialize_extreme_values():
    """Test deserialization with very large and very small float values."""
    # Valeurs extrêmes mais valides
    large_val = 1e30
    small_val = 1e-30
    
    points = [(large_val, small_val), (-large_val, -small_val)]
    data = serialize_pointset(points)
    result = deserialize_pointset(data)
    
    assert len(result) == 2
    assert result[0][0] == pytest.approx(large_val, rel=1e-5)
    assert result[0][1] == pytest.approx(small_val, rel=1e-5)


def test_deserialize_with_infinity():
    """Test deserialization with infinity values."""
    inf = float('inf')
    points = [(inf, 0.0), (0.0, -inf)]
    data = serialize_pointset(points)
    result = deserialize_pointset(data)
    
    assert result[0][0] == inf
    assert result[1][1] == -inf


def test_deserialize_with_nan():
    """Test deserialization with NaN values."""
    import math
    nan = float('nan')
    points = [(nan, 0.0)]
    data = serialize_pointset(points)
    result = deserialize_pointset(data)
    
    assert math.isnan(result[0][0])
    assert result[0][1] == 0.0


# ==================== Tests de buffers corrompus ====================

def test_deserialize_truncated_header():
    """Test deserialization with truncated header."""
    data = b"\x00\x00"  # Seulement 2 bytes au lieu de 4
    with pytest.raises(ValueError, match="too short"):
        deserialize_pointset(data)


def test_deserialize_truncated_data():
    """Test deserialization with truncated point data."""
    # Dit qu'il y a 2 points mais ne fournit que 1 point
    data = b"\x00\x00\x00\x02" + b"\x00" * 8  # 2 points déclarés, 1 fourni
    with pytest.raises(ValueError, match="too short"):
        deserialize_pointset(data)


def test_deserialize_empty_buffer():
    """Test deserialization with empty buffer."""
    data = b""
    with pytest.raises(ValueError, match="too short"):
        deserialize_pointset(data)


def test_deserialize_inconsistent_count():
    """Test deserialization when byte count doesn't match point count."""
    # 3 points déclarés mais seulement 2 fournis
    data = (
        b"\x00\x00\x00\x03"  # 3 points
        b"\x00\x00\x00\x00\x00\x00\x00\x00"  # point 1
        b"\x00\x00\x00\x00\x00\x00\x00\x00"  # point 2
        # point 3 manquant
    )
    with pytest.raises(ValueError, match="too short"):
        deserialize_pointset(data)


# ==================== Tests de sérialisation des Triangles ====================

def test_serialize_triangles_empty():
    """Test serialization with no triangles."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = []
    data = serialize_triangles(vertices, triangles)
    
    # Vérifier la partie vertices
    num_vertices = int.from_bytes(data[:4], byteorder="big")
    assert num_vertices == 3
    
    # Vérifier la partie triangles (après les vertices)
    offset = 4 + 8 * 3  # header + vertices
    num_triangles = int.from_bytes(data[offset:offset+4], byteorder="big")
    assert num_triangles == 0


def test_serialize_triangles_single():
    """Test serialization with one triangle."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]
    data = serialize_triangles(vertices, triangles)
    
    # Vérifier structure complète
    offset = 4 + 8 * 3
    num_triangles = int.from_bytes(data[offset:offset+4], byteorder="big")
    assert num_triangles == 1
    
    # Vérifier les indices
    idx0 = int.from_bytes(data[offset+4:offset+8], byteorder="big")
    idx1 = int.from_bytes(data[offset+8:offset+12], byteorder="big")
    idx2 = int.from_bytes(data[offset+12:offset+16], byteorder="big")
    assert (idx0, idx1, idx2) == (0, 1, 2)


def test_serialize_triangles_multiple():
    """Test serialization with multiple triangles."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = [(0, 1, 2), (0, 2, 3)]
    data = serialize_triangles(vertices, triangles)
    
    offset = 4 + 8 * 4
    num_triangles = int.from_bytes(data[offset:offset+4], byteorder="big")
    assert num_triangles == 2
    
    # Vérifier que la taille totale est correcte
    expected_size = (
        4 + 8 * 4 +  # vertices
        4 + 12 * 2   # triangles
    )
    assert len(data) == expected_size


def test_serialize_triangles_consistency():
    """Test that triangle indices reference valid vertices."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]
    data = serialize_triangles(vertices, triangles)
    
    # Désérialiser pour vérifier la cohérence
    num_vertices = int.from_bytes(data[:4], byteorder="big")
    offset = 4 + 8 * num_vertices + 4
    
    for _ in range(1):  # 1 triangle
        idx0 = int.from_bytes(data[offset:offset+4], byteorder="big")
        idx1 = int.from_bytes(data[offset+4:offset+8], byteorder="big")
        idx2 = int.from_bytes(data[offset+8:offset+12], byteorder="big")
        
        # Tous les indices doivent être < num_vertices
        assert idx0 < num_vertices
        assert idx1 < num_vertices
        assert idx2 < num_vertices
        offset += 12


# ==================== Tests d'indices invalides ====================

def test_serialize_triangles_invalid_negative_index():
    """Test serialization handles negative indices."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(-1, 1, 2)]  # Indice négatif
    
    # Devrait lever une exception avec la nouvelle validation
    with pytest.raises(ValueError, match="Negative index"):
        serialize_triangles(vertices, triangles)


def test_serialize_triangles_out_of_bounds_index():
    """Test that out-of-bounds indices raise an error."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 10)]  # Indice 10 hors limites (max = 2)
    
    # Devrait lever une exception avec la nouvelle validation
    with pytest.raises(ValueError, match="out of bounds"):
        serialize_triangles(vertices, triangles)