#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------


from ram_concept.area_load import AreaLoad
from ram_concept.cad_manager import CadManager
from ram_concept.force_loading_layer import ForceLoadingLayer
from ram_concept.line_load import DefaultLineLoad
from ram_concept.line_load import LineLoad
from ram_concept.line_segment_2D import LineSegment2D
from ram_concept.model import Model
from ram_concept.point_load import PointLoad
from ram_concept.point_2D import Point2D
from ram_concept.polygon_2D import Polygon2D
from ram_concept.slab_area import SlabArea

def add_loads(model: Model):
    """Adds loads to the 16m x 16m structure """

    # The structure created is a simple 16m x 16m square, with 8m spans:

    #  cbbbbbbbcbbbbbbbc
    #  |               |
    #  |               |
    #  w       c       w
    #  w               w
    #  w               w
    #  wwwwwwwwwwwwwwwww

    # in this code, we depend upon the standard loading names, we could also find loading by looking at their loading types instead
    # note that new loadings can be added and (most) loadings can be deleted

    # in addition to self-dead, we want to add Other Dead and Reducible live loadings

    cad_manager = model.cad_manager
    dead_ldg = cad_manager.force_loading_layer("Other Dead Loading")
    live_ldg = cad_manager.force_loading_layer("Live (Reducible) Loading")

    # for convenience below
    corner_pt1 = Point2D( 0, 0)
    corner_pt2 = Point2D(16, 0)
    corner_pt3 = Point2D(16,16)
    corner_pt4 = Point2D( 0,16)

    # ADD A PERIMETER DEAD LOAD

    default_line_load = cad_manager.default_line_load

    default_line_load.elevation = 0
    default_line_load.set_load_values(0,0,-10000,0,0) # remember we set signs all positive...so negative Fz load is downward

    dead_ldg.add_line_load(LineSegment2D(corner_pt1, corner_pt2))
    dead_ldg.add_line_load(LineSegment2D(corner_pt2, corner_pt3))
    dead_ldg.add_line_load(LineSegment2D(corner_pt3, corner_pt4))
    dead_ldg.add_line_load(LineSegment2D(corner_pt4, corner_pt1))

    # ADD UNIFORM DEAD LOAD

    whole_slab_polygon = Polygon2D([corner_pt1, corner_pt2, corner_pt3, corner_pt4])

    dead_area_load = dead_ldg.add_area_load(whole_slab_polygon)
    dead_area_load.elevation = 0
    dead_area_load.set_load_values(0,0,-2000,0,0)

    # ADD UNIFORM LIVE LOAD

    live_area_load = live_ldg.add_area_load(whole_slab_polygon)
    live_area_load.elevation = 0
    live_area_load.set_load_values(0,0,-5000,0,0)

    # ADD POINT LIVE LOAD (just to complete the example)

    live_point_load = live_ldg.add_point_load(Point2D(12,12))
    live_point_load.elevation = 0
    live_point_load.zero_load_values()
    live_point_load.Fz = -50000
    
