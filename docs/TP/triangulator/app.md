Module TP.triangulator.app
==========================
Application Flask pour le service de triangulation.

Functions
---------

`get_triangulation(pointset_id)`
:   Calculate the triangulation of a PointSet given its ID.
    
    Args:
        pointset_id: UUID of the PointSet to triangulate
        
    Returns:
        Binary response containing triangulated data, or JSON error

`method_not_allowed(e)`
:   Handle 405 Method Not Allowed errors.

`not_found(e)`
:   Handle 404 errors.