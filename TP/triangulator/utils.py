"""Module pour la triangulation de points 2D."""
import struct


def serialize_pointset(pointset):
    """Serialize a PointSet to binary format (float32)."""
    if not pointset:
        return b"\x00\x00\x00\x00"  # 4 bytes pour 0 points

    num_points = len(pointset)
    data = num_points.to_bytes(4, byteorder='big')

    for x, y in pointset:
        data += struct.pack('>f', float(x))  # X en float32 big-endian
        data += struct.pack('>f', float(y))  # Y en float32 big-endian

    return data

def deserialize_pointset(data):
    """Deserialize binary data to list of (x, y) float tuples."""
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
    """Serialize vertices + triangles into binary format."""
    # Part 1: serialize vertices (same as PointSet)
    vertex_data = serialize_pointset(vertices)
    
    # Part 2: serialize triangles
    num_triangles = len(triangles)
    triangle_data = num_triangles.to_bytes(4, byteorder='big')
    for i, j, k in triangles:
        triangle_data += i.to_bytes(4, byteorder='big')
        triangle_data += j.to_bytes(4, byteorder='big')
        triangle_data += k.to_bytes(4, byteorder='big')
    
    return vertex_data + triangle_data