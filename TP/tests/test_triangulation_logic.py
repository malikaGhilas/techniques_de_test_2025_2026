"""Tests for the core triangulation logic."""

from triangulator.services import triangulate

# ==================== Tests de base ====================

def test_triangulate_function_exists():
    """Vérifie que la fonction triangulate existe."""
    assert triangulate is not None


def test_triangulate_empty_pointset():
    """Test triangulation with empty point set."""
    points = []
    triangles = triangulate(points)
    assert triangles == []


def test_triangulate_single_point():
    """Test triangulation with single point (non-triangulable)."""
    points = [(0.0, 0.0)]
    triangles = triangulate(points)
    assert triangles == []


def test_triangulate_two_points():
    """Test triangulation with two points (non-triangulable)."""
    points = [(0.0, 0.0), (1.0, 1.0)]
    triangles = triangulate(points)
    assert triangles == []


# ==================== Tests de cas simples ====================

def test_triangulate_three_points():
    """Test triangulation with exactly 3 points (1 triangle)."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = triangulate(points)
    
    # Avec 3 points, on doit avoir exactement 1 triangle
    assert len(triangles) == 1
    
    # Vérifier que les indices sont valides
    for i, j, k in triangles:
        assert 0 <= i < len(points)
        assert 0 <= j < len(points)
        assert 0 <= k < len(points)


def test_triangulate_four_points():
    """Test triangulation with 4 points (2 triangles expected)."""
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = triangulate(points)
    
    # Fan triangulation : n-2 triangles pour n points
    assert len(triangles) == 2
    
    # Vérifier les indices
    for i, j, k in triangles:
        assert 0 <= i < len(points)
        assert 0 <= j < len(points)
        assert 0 <= k < len(points)


def test_triangulate_five_points():
    """Test triangulation with 5 points (3 triangles expected)."""
    points = [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (1.0, 2.0), (0.0, 1.0)]
    triangles = triangulate(points)
    
    assert len(triangles) == 3
    
    for i, j, k in triangles:
        assert 0 <= i < len(points)
        assert 0 <= j < len(points)
        assert 0 <= k < len(points)


# ==================== Tests de propriétés structurelles ====================

def test_triangulate_all_points_used():
    """Test that all input points appear in at least one triangle."""
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = triangulate(points)
    
    # Collecter tous les indices utilisés
    used_indices = set()
    for i, j, k in triangles:
        used_indices.add(i)
        used_indices.add(j)
        used_indices.add(k)
    
    # Tous les points doivent être utilisés
    assert used_indices == set(range(len(points)))


def test_triangulate_no_duplicate_triangles():
    """Test that no triangle appears twice."""
    points = [(i * 0.5, i * 0.3) for i in range(10)]
    triangles = triangulate(points)
    
    # Normaliser les triangles (trier les indices pour comparaison)
    normalized = [tuple(sorted([i, j, k])) for i, j, k in triangles]
    
    # Vérifier qu'il n'y a pas de doublons
    assert len(normalized) == len(set(normalized))


def test_triangulate_valid_indices():
    """Test that all triangle indices are within valid range."""
    points = [(i * 1.0, i * 0.5) for i in range(20)]
    triangles = triangulate(points)
    
    for i, j, k in triangles:
        assert 0 <= i < len(points), f"Index {i} out of range"
        assert 0 <= j < len(points), f"Index {j} out of range"
        assert 0 <= k < len(points), f"Index {k} out of range"


def test_triangulate_distinct_vertices():
    """Test that each triangle has 3 distinct vertices."""
    points = [(i * 0.7, i * 0.4) for i in range(15)]
    triangles = triangulate(points)
    
    for i, j, k in triangles:
        assert i != j, f"Triangle has duplicate vertices: ({i}, {j}, {k})"
        assert j != k, f"Triangle has duplicate vertices: ({i}, {j}, {k})"
        assert i != k, f"Triangle has duplicate vertices: ({i}, {j}, {k})"


# ==================== Tests de déterminisme ====================

def test_triangulate_deterministic():
    """Test that triangulation is deterministic (same input → same output)."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0), (1.5, 0.5)]
    
    triangles1 = triangulate(points)
    triangles2 = triangulate(points)
    
    assert triangles1 == triangles2


# ==================== Tests avec points intérieurs ====================

def test_triangulate_with_interior_point():
    """Test triangulation with a point inside the convex hull."""
    # Carré avec un point au centre
    points = [
        (0.0, 0.0),  # coin bas-gauche
        (2.0, 0.0),  # coin bas-droit
        (2.0, 2.0),  # coin haut-droit
        (0.0, 2.0),  # coin haut-gauche
        (1.0, 1.0),  # centre
    ]
    triangles = triangulate(points)
    
    # Doit produire des triangles (nombre dépend de l'algo)
    assert len(triangles) == 3  # n-2 pour fan triangulation
    
    # Tous les points doivent être utilisés
    used = set()
    for i, j, k in triangles:
        used.update([i, j, k])
    assert len(used) == len(points)


# ==================== Tests de cas dégénérés ====================

def test_triangulate_collinear_points():
    """Test triangulation with collinear points (should handle gracefully)."""
    # 3 points alignés horizontalement
    points = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
    triangles = triangulate(points)
    
    # Comportement attendu : soit [] soit [un triangle dégénéré]
    # Selon votre implémentation, accepter les deux
    assert isinstance(triangles, list)
    
    if len(triangles) > 0:
        # Si un triangle est créé, vérifier qu'il a des indices valides
        for i, j, k in triangles:
            assert 0 <= i < len(points)
            assert 0 <= j < len(points)
            assert 0 <= k < len(points)


def test_triangulate_duplicate_points():
    """Test triangulation with duplicate points."""
    # Points avec doublons
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 0.0)]
    triangles = triangulate(points)
    
    # Doit gérer sans planter
    assert isinstance(triangles, list)
    
    # Vérifier que les indices sont valides
    for i, j, k in triangles:
        assert 0 <= i < len(points)
        assert 0 <= j < len(points)
        assert 0 <= k < len(points)


def test_triangulate_very_close_points():
    """Test triangulation with points very close to each other."""
    epsilon = 1e-10
    points = [
        (0.0, 0.0),
        (epsilon, 0.0),
        (0.0, epsilon),
        (1.0, 1.0),
    ]
    triangles = triangulate(points)
    
    # Doit produire un résultat (même si numériquement instable)
    assert isinstance(triangles, list)
    assert len(triangles) >= 0


# ==================== Tests géométriques ====================

def calculate_triangle_area(p1, p2, p3):
    """Calculate area of triangle using cross product."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2.0


def test_triangulate_non_degenerate_triangles():
    """Test that triangles have non-zero area (for non-collinear points)."""
    # Points bien espacés (non-colinéaires)
    points = [
        (0.0, 0.0),
        (2.0, 0.0),
        (1.0, 2.0),
        (3.0, 1.0),
    ]
    triangles = triangulate(points)
    
    for i, j, k in triangles:
        area = calculate_triangle_area(points[i], points[j], points[k])
        # Pour des points non-colinéaires, l'aire doit être > 0
        # On tolère une petite marge pour les erreurs numériques
        assert area > 1e-10, f"Triangle ({i},{j},{k}) has zero area"


# ==================== Tests avec points aléatoires ====================

def test_triangulate_random_points():
    """Test triangulation with random-like distributed points."""
    import random
    random.seed(42)  # Pour reproductibilité
    
    points = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(30)]
    triangles = triangulate(points)
    
    # Vérifier propriétés de base
    assert len(triangles) == len(points) - 2  # Fan triangulation
    
    # Tous les indices valides
    for i, j, k in triangles:
        assert 0 <= i < len(points)
        assert 0 <= j < len(points)
        assert 0 <= k < len(points)
        assert len({i, j, k}) == 3  # 3 vertices distincts


# ==================== Tests de formule n-2 ====================

def test_triangulate_formula_n_minus_2():
    """Test that fan triangulation produces exactly n-2 triangles."""
    for n in [3, 4, 5, 10, 20, 50]:
        points = [(i * 0.1, i * 0.2) for i in range(n)]
        triangles = triangulate(points)
        expected = n - 2
        assert len(triangles) == expected, \
            f"Expected {expected} triangles for {n} points, got {len(triangles)}"