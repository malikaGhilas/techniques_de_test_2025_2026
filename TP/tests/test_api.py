"""Tests for the Triangulator API endpoints."""
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
