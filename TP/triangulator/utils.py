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
        raise ValueError(f"Data too short: expected {expected_length} bytes, got {len(data)}")
    
    points = []
    offset = 4
    for _ in range(num_points):
        x = struct.unpack('>f', data[offset:offset+4])[0]
        y = struct.unpack('>f', data[offset+4:offset+8])[0]
        points.append((x, y))
        offset += 8
    return points