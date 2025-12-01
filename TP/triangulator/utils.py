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