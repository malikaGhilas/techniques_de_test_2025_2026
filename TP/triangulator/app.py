"""Application Flask pour le service de triangulation."""
from flask import Flask, Response

from .services import fetch_pointset_from_manager, triangulate
from .utils import deserialize_pointset, serialize_triangles

app = Flask(__name__)

@app.route('/triangulation/<pointset_id>', methods=['GET'])
def get_triangulation(pointset_id):
    """Calculate the triangulation of a PointSet given its ID."""
    try:
        pointset_bytes = fetch_pointset_from_manager(pointset_id, use_mock=True)
        points = deserialize_pointset(pointset_bytes)
        triangles = triangulate(points)
        result_bytes = serialize_triangles(points, triangles)
        return Response(result_bytes, mimetype='application/octet-stream')
    except Exception as e:
        return {"code": "INTERNAL_ERROR", "message": str(e)}, 500