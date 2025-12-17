Module TP.triangulator.services
===============================
Module pour la triangulation de points 2D.

Functions
---------

`fetch_pointset_from_manager(pointset_id: str, use_mock: bool = True) ‑> bytes`
:   Fetch PointSet binary data from PointSetManager.

`triangulate(pointset)`
:   Naive fan triangulation.
    
    Returns list of triangles as (i, j, k) indices.