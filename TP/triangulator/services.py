"""Module pour la triangulation de points 2D."""
import urllib.error
import urllib.request


def fetch_pointset_from_manager(pointset_id: str, use_mock: bool = True) -> bytes:
    """Fetch PointSet binary data from PointSetManager."""
    if use_mock:
         return (
            b"\x00\x00\x00\x03"
            b"\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x3f\x80\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x3f\x80\x00\x00"
        )
    url = f"http://pointset-manager:5000/pointsets/{pointset_id}"
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP error {e.code} for {url}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"URL error for {url}: {e}") from e

def triangulate(pointset):
    """Naive fan triangulation.

    Returns list of triangles as (i, j, k) indices.
    """
    if len(pointset) < 3:
        return []
    triangles = []
    for i in range(1, len(pointset) - 1):
        triangles.append((0, i, i + 1))
    return triangles