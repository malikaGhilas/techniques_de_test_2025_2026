"""Performance tests for triangulation (marked as slow)."""
import time

import pytest
from triangulator.services import triangulate
from triangulator.utils import (
    deserialize_pointset,
    serialize_pointset,
    serialize_triangles,
)

# ==================== Tests de performance de triangulation ====================

@pytest.mark.slow
def test_triangulate_100_points():
    """Triangulate 100 points and measure time."""
    points = [(float(i % 10), float(i // 10)) for i in range(100)]
    start = time.perf_counter()
    triangles = triangulate(points)
    duration = time.perf_counter() - start
    print(f"\n100 points → {len(triangles)} triangles in {duration:.4f}s")
    assert len(triangles) == 98  # fan triangulation: n-2 triangles
    assert duration < 0.1, f"Too slow: {duration:.4f}s"


@pytest.mark.slow
def test_triangulate_1000_points():
    """Triangulate 1000 points and measure time."""
    points = [(float(i % 32), float(i // 32)) for i in range(1000)]
    start = time.perf_counter()
    triangles = triangulate(points)
    duration = time.perf_counter() - start
    print(f"\n1000 points → {len(triangles)} triangles in {duration:.4f}s")
    assert len(triangles) == 998
    assert duration < 0.5, f"Too slow: {duration:.4f}s"


@pytest.mark.slow
def test_triangulate_10000_points():
    """Triangulate 10000 points and measure time."""
    points = [(float(i % 100), float(i // 100)) for i in range(10000)]
    start = time.perf_counter()
    triangles = triangulate(points)
    duration = time.perf_counter() - start
    print(f"\n10000 points → {len(triangles)} triangles in {duration:.4f}s")
    assert len(triangles) == 9998
    assert duration < 5.0, f"Too slow: {duration:.4f}s"


# ==================== Tests de performance de sérialisation ====================

@pytest.mark.slow
def test_serialize_large_pointset():
    """Test serialization performance with large PointSet."""
    points = [(float(i), float(i * 2)) for i in range(10000)]
    
    start = time.perf_counter()
    data = serialize_pointset(points)
    duration = time.perf_counter() - start
    
    print(f"\nSerialized 10000 points in {duration:.4f}s")
    assert len(data) == 4 + 8 * 10000
    assert duration < 0.5, f"Serialization too slow: {duration:.4f}s"


@pytest.mark.slow
def test_deserialize_large_pointset():
    """Test deserialization performance with large PointSet."""
    points = [(float(i), float(i * 2)) for i in range(10000)]
    data = serialize_pointset(points)
    
    start = time.perf_counter()
    result = deserialize_pointset(data)
    duration = time.perf_counter() - start
    
    print(f"\nDeserialized 10000 points in {duration:.4f}s")
    assert len(result) == 10000
    assert duration < 0.5, f"Deserialization too slow: {duration:.4f}s"


@pytest.mark.slow
def test_serialize_triangles_large():
    """Test serialization of large triangle set."""
    points = [(float(i % 100), float(i // 100)) for i in range(1000)]
    triangles = triangulate(points)
    
    start = time.perf_counter()
    data = serialize_triangles(points, triangles)
    duration = time.perf_counter() - start
    
    print(f"\nSerialized {len(triangles)} triangles in {duration:.4f}s")
    expected_size = 4 + 8 * 1000 + 4 + 12 * len(triangles)
    assert len(data) == expected_size
    assert duration < 0.5, f"Triangle serialization too slow: {duration:.4f}s"


# ==================== Tests de performance de roundtrip complet ====================

@pytest.mark.slow
def test_full_roundtrip_performance():
    """Test complete serialize→deserialize→triangulate→serialize cycle."""
    # Créer des points
    points = [(float(i * 0.1), float(i * 0.2)) for i in range(500)]
    
    # Mesurer le cycle complet
    start = time.perf_counter()
    
    # 1. Sérialiser les points
    serialized_points = serialize_pointset(points)
    
    # 2. Désérialiser
    deserialized_points = deserialize_pointset(serialized_points)
    
    # 3. Trianguler
    triangles = triangulate(deserialized_points)
    
    # 4. Sérialiser le résultat
    _ = serialize_triangles(deserialized_points, triangles)
    
    duration = time.perf_counter() - start
    
    print(f"\nFull roundtrip (500 points) in {duration:.4f}s")
    assert len(triangles) == 498
    assert duration < 1.0, f"Full cycle too slow: {duration:.4f}s"


# ==================== Tests de scalabilité ====================

@pytest.mark.slow
def test_scalability_triangulation():
    """Test how triangulation time scales with input size."""
    sizes = [10, 50, 100, 500, 1000]
    times = []
    
    print("\nScalability test:")
    for size in sizes:
        points = [(float(i * 0.1), float(i * 0.2)) for i in range(size)]
        
        start = time.perf_counter()
        triangles = triangulate(points)
        duration = time.perf_counter() - start
        
        times.append(duration)
        print(f"  {size} points: {duration:.4f}s ({len(triangles)} triangles)")
        
        assert len(triangles) == size - 2
    
    # Vérifier que c'est à peu près linéaire (fan triangulation est O(n))
    # Le ratio temps[4] / temps[0] devrait être proche de sizes[4] / sizes[0]
    ratio_time = times[-1] / times[0] if times[0] > 0 else 0
    ratio_size = sizes[-1] / sizes[0]
    
    # Accepter un ratio jusqu'à 2x la croissance linéaire (O(n) à O(n log n))
    assert ratio_time < ratio_size * 2, f"Growth rate too high: {ratio_time:.2f}x"


# ==================== Tests de mémoire (indicatif) ====================

@pytest.mark.slow
def test_memory_efficiency():
    """Test that serialization doesn't use excessive memory."""
    # Créer un grand jeu de points
    points = [(float(i), float(i)) for i in range(10000)]
    
    # Sérialiser
    data = serialize_pointset(points)
    
    # Vérifier que la taille est exactement ce qu'on attend (pas de gaspillage)
    expected_size = 4 + 8 * len(points)
    assert len(data) == expected_size
    
    # Calculer l'efficacité : bytes par point
    bytes_per_point = len(data) / len(points)
    print(f"\nMemory efficiency: {bytes_per_point:.2f} bytes/point")
    assert bytes_per_point < 9.0  # Devrait être proche de 8