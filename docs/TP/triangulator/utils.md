Module TP.triangulator.utils
============================
Module pour la sérialisation/désérialisation de structures géométriques.

Functions
---------

`deserialize_pointset(data)`
:   Deserialize binary data to list of (x, y) float tuples.
    
    Args:
        data: Binary data in the PointSet format
        
    Returns:
        list: List of (x, y) tuples
        
    Raises:
        ValueError: If data is invalid or truncated

`serialize_pointset(pointset)`
:   Serialize a PointSet to binary format (float32).
    
    Args:
        pointset: List of (x, y) tuples representing 2D points
        
    Returns:
        bytes: Binary representation in big-endian format

`serialize_triangles(vertices, triangles)`
:   Serialize vertices + triangles into binary format.
    
    Args:
        vertices: List of (x, y) tuples representing vertices
        triangles: List of (i, j, k) tuples representing triangle indices
        
    Returns:
        bytes: Binary representation of the complete triangulation
        
    Raises:
        ValueError: If triangle indices are invalid