"""Application Flask pour le service de triangulation."""
from flask import Flask, Response, jsonify

from .services import fetch_pointset_from_manager, triangulate
from .utils import deserialize_pointset, serialize_triangles

app = Flask(__name__)


@app.route('/triangulation/<pointset_id>', methods=['GET'])
def get_triangulation(pointset_id):
    """Calculate the triangulation of a PointSet given its ID.
    
    Args:
        pointset_id: UUID of the PointSet to triangulate
        
    Returns:
        Binary response containing triangulated data, or JSON error

    """
    try:
        # Fetch PointSet from manager
        pointset_bytes = fetch_pointset_from_manager(pointset_id, use_mock=True)
        
        # Deserialize to points
        points = deserialize_pointset(pointset_bytes)
        
        # Check if we have enough points
        if len(points) < 3:
            return jsonify({
                "code": "INSUFFICIENT_POINTS",
                "message": (
                    f"Need at least 3 points for triangulation, "
                    f"got {len(points)}"
                )
            }), 400
        
        # Triangulate
        triangles = triangulate(points)
        
        # Serialize result
        result_bytes = serialize_triangles(points, triangles)
        
        return Response(result_bytes, mimetype='application/octet-stream')
        
    except ValueError as e:
        # Erreurs de désérialisation
        return jsonify({
            "code": "INVALID_DATA",
            "message": f"Invalid PointSet data: {str(e)}"
        }), 400
        
    except RuntimeError as e:
        # Erreurs de communication avec PointSetManager
        error_msg = str(e).lower()
        
        if "404" in error_msg or "not found" in error_msg:
            return jsonify({
                "code": "NOT_FOUND",
                "message": f"PointSet {pointset_id} not found"
            }), 404
            
        elif "503" in error_msg or "unavailable" in error_msg:
            return jsonify({
                "code": "SERVICE_UNAVAILABLE",
                "message": "PointSetManager service is unavailable"
            }), 503
            
        else:
            return jsonify({
                "code": "UPSTREAM_ERROR",
                "message": f"Error communicating with PointSetManager: {str(e)}"
            }), 502
            
    except Exception as e:
        # Erreur inattendue
        return jsonify({
            "code": "INTERNAL_ERROR",
            "message": f"Internal server error: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        "code": "NOT_FOUND",
        "message": "The requested resource was not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 Method Not Allowed errors."""
    return jsonify({
        "code": "METHOD_NOT_ALLOWED",
        "message": "The HTTP method is not allowed for this endpoint"
    }), 405