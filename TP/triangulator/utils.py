"""Module pour la sérialisation/désérialisation de structures géométriques."""
import struct


def serialize_pointset(pointset):
    """Serialize a PointSet to binary format (float32).
    
    Args:
        pointset: List of (x, y) tuples representing 2D points
        
    Returns:
        bytes: Binary representation in big-endian format

    """
    if not pointset:
        return b"\x00\x00\x00\x00"  # 4 bytes pour 0 points

    num_points = len(pointset)
    data = num_points.to_bytes(4, byteorder='big')

    for x, y in pointset:
        data += struct.pack('>f', float(x))  # X en float32 big-endian
        data += struct.pack('>f', float(y))  # Y en float32 big-endian

    return data


def deserialize_pointset(data):
    """Deserialize binary data to list of (x, y) float tuples.
    
    Args:
        data: Binary data in the PointSet format
        
    Returns:
        list: List of (x, y) tuples
        
    Raises:
        ValueError: If data is invalid or truncated

    """
    if len(data) < 4:
        raise ValueError("Data too short to contain point count")
    
    num_points = int.from_bytes(data[:4], byteorder='big')
    
    if num_points == 0:
        return []
    
    expected_length = 4 + 8 * num_points
    if len(data) < expected_length:
        msg = f"Data too short: expected {expected_length} bytes, "
        msg += f"got {len(data)}"
        raise ValueError(msg)
    
    points = []
    offset = 4
    for _ in range(num_points):
        x = struct.unpack('>f', data[offset:offset+4])[0]
        y = struct.unpack('>f', data[offset+4:offset+8])[0]
        points.append((x, y))
        offset += 8
    
    return points


def serialize_triangles(vertices, triangles):
    """Serialize vertices + triangles into binary format.
    
    Args:
        vertices: List of (x, y) tuples representing vertices
        triangles: List of (i, j, k) tuples representing triangle indices
        
    Returns:
        bytes: Binary representation of the complete triangulation
        
    Raises:
        ValueError: If triangle indices are invalid

    """
    # Part 1: serialize vertices (same as PointSet)
    vertex_data = serialize_pointset(vertices)
    
    # Part 2: serialize triangles
    num_triangles = len(triangles)
    triangle_data = num_triangles.to_bytes(4, byteorder='big')
    
    num_vertices = len(vertices)
    for i, j, k in triangles:
        # Validation des indices
        if i < 0 or j < 0 or k < 0:
            raise ValueError(f"Negative index in triangle: ({i}, {j}, {k})")
        if i >= num_vertices or j >= num_vertices or k >= num_vertices:
            raise ValueError(
                f"Index out of bounds in triangle ({i}, {j}, {k}), "
                f"max index is {num_vertices - 1}"
            )
        
        triangle_data += i.to_bytes(4, byteorder='big')
        triangle_data += j.to_bytes(4, byteorder='big')
        triangle_data += k.to_bytes(4, byteorder='big')
    
    return vertex_data + triangle_data