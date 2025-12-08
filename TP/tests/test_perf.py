"""Performance tests for triangulation (marked as slow)."""
import time

import pytest
from triangulator.services import triangulate


@pytest.mark.slow
def test_triangulate_100_points():
    """Triangulate 100 points and measure time."""
    points = [(float(i % 10), float(i // 10)) for i in range(100)]
    start = time.perf_counter()
    triangles = triangulate(points)
    duration = time.perf_counter() - start
    print(f"\n100 points → {len(triangles)} triangles in {duration:.4f}s")
    assert len(triangles) == 98  # fan triangulation: n-2 triangles

@pytest.mark.slow
def test_triangulate_1000_points():
    """Triangulate 1000 points and measure time."""
    points = [(float(i % 32), float(i // 32)) for i in range(1000)]
    start = time.perf_counter()
    triangles = triangulate(points)
    duration = time.perf_counter() - start
    print(f"\n1000 points → {len(triangles)} triangles in {duration:.4f}s")
    assert len(triangles) == 998