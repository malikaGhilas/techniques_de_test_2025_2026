"""Tests for the Triangulator API endpoints."""
from unittest.mock import patch

import pytest
from triangulator.app import app


def test_app_exists():
    """Vérifie que l'application Flask est bien créée."""
    assert app is not None


@pytest.fixture
def client():
    """Fournit un client de test pour l'application Flask."""
    with app.test_client() as client:
        yield client


# ==================== Tests du happy path ====================

def test_triangulation_happy_path(client):
    """Test avec 3 points → 1 triangle."""
    response = client.get('/triangulation/test-id')
    
    assert response.status_code == 200
    assert response.mimetype == 'application/octet-stream'
    
    data = response.data
    # 3 points → 4 + 24 = 28 bytes
    # 1 triangle → 4 + 12 = 16 bytes
    # Total = 44 bytes
    assert len(data) == 44

    num_points = int.from_bytes(data[:4], byteorder='big')
    assert num_points == 3

    num_triangles = int.from_bytes(data[28:32], byteorder='big')
    assert num_triangles == 1

    # Vérifier les indices du triangle (doit être (0,1,2))
    idx0 = int.from_bytes(data[32:36], 'big')
    idx1 = int.from_bytes(data[36:40], 'big')
    idx2 = int.from_bytes(data[40:44], 'big')
    assert (idx0, idx1, idx2) == (0, 1, 2)


def test_triangulation_with_4_points(client):
    """Test avec 4 points → 2 triangles."""
    # Mock pour retourner 4 points
    mock_data = (
        b"\x00\x00\x00\x04"  # 4 points
        b"\x00\x00\x00\x00\x00\x00\x00\x00"  # (0, 0)
        b"\x3f\x80\x00\x00\x00\x00\x00\x00"  # (1, 0)
        b"\x3f\x80\x00\x00\x3f\x80\x00\x00"  # (1, 1)
        b"\x00\x00\x00\x00\x3f\x80\x00\x00"  # (0, 1)
    )
    
    with patch('triangulator.app.fetch_pointset_from_manager', return_value=mock_data):
        response = client.get('/triangulation/test-id')
        
        assert response.status_code == 200
        data = response.data
        
        num_points = int.from_bytes(data[:4], byteorder='big')
        assert num_points == 4
        
        offset = 4 + 8 * 4  # après les vertices
        num_triangles = int.from_bytes(data[offset:offset+4], byteorder='big')
        assert num_triangles == 2  # Fan: n-2 = 4-2 = 2


# ==================== Tests de validation des headers HTTP ====================

def test_response_headers(client):
    """Test que les headers HTTP sont corrects."""
    response = client.get('/triangulation/test-id')
    
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/octet-stream'
    assert 'Content-Length' in response.headers
    assert int(response.headers['Content-Length']) == len(response.data)


# ==================== Tests de méthodes HTTP non autorisées ====================

def test_method_not_allowed_post(client):
    """Test que POST n'est pas autorisé sur /triangulation."""
    response = client.post('/triangulation/test-id')
    assert response.status_code == 405  # Method Not Allowed


def test_method_not_allowed_put(client):
    """Test que PUT n'est pas autorisé sur /triangulation."""
    response = client.put('/triangulation/test-id')
    assert response.status_code == 405


def test_method_not_allowed_delete(client):
    """Test que DELETE n'est pas autorisé sur /triangulation."""
    response = client.delete('/triangulation/test-id')
    assert response.status_code == 405


# ==================== Tests de routes inconnues ====================

def test_unknown_route_returns_404(client):
    """Test qu'une route inconnue retourne 404."""
    response = client.get('/unknown/path')
    assert response.status_code == 404


def test_root_route_returns_404(client):
    """Test que la racine retourne 404."""
    response = client.get('/')
    assert response.status_code == 404


# ==================== Tests d'erreurs du PointSetManager ====================

@patch('triangulator.app.fetch_pointset_from_manager')
def test_pointset_not_found_404(mock_fetch, client):
    """Test quand le PointSetManager retourne 404."""
    mock_fetch.side_effect = RuntimeError("HTTP error 404")
    
    response = client.get('/triangulation/nonexistent-id')
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'code' in data
    assert 'message' in data


@patch('triangulator.app.fetch_pointset_from_manager')
def test_pointset_manager_unavailable_503(mock_fetch, client):
    """Test quand le PointSetManager est indisponible."""
    mock_fetch.side_effect = RuntimeError("Service unavailable")
    
    response = client.get('/triangulation/test-id')
    
    assert response.status_code == 503
    data = response.get_json()
    assert 'code' in data
    assert 'message' in data


@patch('triangulator.app.fetch_pointset_from_manager')
def test_pointset_manager_internal_error(mock_fetch, client):
    """Test quand le PointSetManager a une erreur interne."""
    mock_fetch.side_effect = RuntimeError("Internal server error")
    
    response = client.get('/triangulation/test-id')
    assert response.status_code == 502


# ==================== Tests de données invalides ====================

@patch('triangulator.app.fetch_pointset_from_manager')
def test_corrupted_data_from_manager(mock_fetch, client):
    """Test avec des données corrompues du PointSetManager."""
    # Buffer tronqué/invalide
    mock_fetch.return_value = b"\x00\x00\x00\x05"  # Dit 5 points mais pas de données
    
    response = client.get('/triangulation/test-id')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'code' in data


@patch('triangulator.app.fetch_pointset_from_manager')
def test_empty_pointset(mock_fetch, client):
    """Test avec un PointSet vide."""
    mock_fetch.return_value = b"\x00\x00\x00\x00"  # 0 points
    
    response = client.get('/triangulation/test-id')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'code' in data
    assert 'INSUFFICIENT_POINTS' in data['code']


@patch('triangulator.app.fetch_pointset_from_manager')
def test_insufficient_points_for_triangulation(mock_fetch, client):
    """Test avec moins de 3 points (non-triangulable)."""
    # 2 points seulement
    mock_fetch.return_value = (
        b"\x00\x00\x00\x02"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x3f\x80\x00\x00\x3f\x80\x00\x00"
    )
    
    response = client.get('/triangulation/test-id')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'INSUFFICIENT_POINTS' in data['code']


@patch('triangulator.app.fetch_pointset_from_manager')
def test_collinear_points_handling(mock_fetch, client):
    """Test avec des points colinéaires (cas géométrique dégénéré)."""
    # 3 points alignés horizontalement
    mock_fetch.return_value = (
        b"\x00\x00\x00\x03"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"  # (0, 0)
        b"\x3f\x80\x00\x00\x00\x00\x00\x00"  # (1, 0)
        b"\x40\x00\x00\x00\x00\x00\x00\x00"  # (2, 0)
    )
    
    response = client.get('/triangulation/test-id')
    
    # Peut accepter et créer un triangle dégénéré
    assert response.status_code == 200


# ==================== Tests de cas limites d'ID ====================

def test_empty_pointset_id(client):
    """Test avec un ID vide."""
    response = client.get('/triangulation/')
    # Flask retourne 404 pour une route sans paramètre
    assert response.status_code == 404


def test_very_long_pointset_id(client):
    """Test avec un ID très long."""
    long_id = 'a' * 1000
    response = client.get(f'/triangulation/{long_id}')
    # Devrait fonctionner normalement
    assert response.status_code in [200, 400, 404, 500]


def test_special_characters_in_id(client):
    """Test avec des caractères spéciaux dans l'ID."""
    special_id = 'test-id/with/slashes'
    response = client.get(f'/triangulation/{special_id}')
    # Flask va interpréter ça comme plusieurs segments de chemin
    assert response.status_code == 404


# ==================== Tests d'intégration bout-en-bout ====================

def test_full_workflow_integration(client):
    """Test du workflow complet : fetch → deserialize → triangulate → serialize."""
    # Utilise le mock par défaut (3 points)
    response = client.get('/triangulation/integration-test')
    
    assert response.status_code == 200
    assert response.mimetype == 'application/octet-stream'
    
    data = response.data
    
    # Vérifier structure complète
    assert len(data) >= 32  # Minimum pour 3 points + header triangles
    
    # Vérifier que c'est un format binaire valide
    num_points = int.from_bytes(data[:4], byteorder='big')
    assert num_points > 0
    
    offset = 4 + 8 * num_points
    num_triangles = int.from_bytes(data[offset:offset+4], byteorder='big')
    assert num_triangles >= 0


# ==================== Tests de performance API ====================

def test_api_response_time(client):
    """Test que l'API répond dans un temps raisonnable."""
    import time
    
    start = time.perf_counter()
    response = client.get('/triangulation/perf-test')
    duration = time.perf_counter() - start
    
    assert response.status_code == 200
    # L'API devrait répondre en moins d'1 seconde pour 3 points
    assert duration < 1.0, f"API took {duration:.2f}s to respond"


# ==================== Tests de concurrence (basique) ====================

def test_multiple_sequential_requests(client):
    """Test de plusieurs requêtes séquentielles."""
    results = []
    for i in range(5):
        response = client.get(f'/triangulation/test-{i}')
        results.append(response.status_code)
    
    # Toutes les requêtes devraient réussir
    assert all(status == 200 for status in results)