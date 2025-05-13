#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# to avoid circular module dependencies, when references only used for type hints
# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import List
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .add_property import _cad_entity_list_property
from .cad_layer import CadLayer
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .area_spring import AreaSpring
    from .beam import Beam
    from .cad_entity import CadEntity
    from .column import Column
    from .model import Model
    from .line_segment_2D import LineSegment2D
    from .line_spring import LineSpring
    from .line_support import LineSupport
    from .point_spring import PointSpring
    from .point_support import PointSupport
    from .point_2D import Point2D
    from .polygon_2D import Polygon2D
    from .slab_area import SlabArea
    from .slab_opening import SlabOpening
    from .wall import Wall

# -------------------------------------------------------------------------------------------------

class StructureLayer(CadLayer):
    """StructureLayer represents the "mesh input" layer in the CAD system.
    
    The structure drawn on the `StructureLayer` is meshed into the finite elements on the :any:`ElementLayer`.
    The StructureLayer is accessible through :any:`CadManager.structure_layer`.
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    point_springs: List[PointSpring]  = _cad_entity_list_property("PointSprings", "All the :any:`PointSpring` on this layer.")
    line_springs:  List[LineSpring]   = _cad_entity_list_property("LineSprings", "All the :any:`LineSpring` on this layer.")
    area_springs:  List[AreaSpring]   = _cad_entity_list_property("AreaSprings", "All the :any:`AreaSpring` on this layer.")

    point_supports: List[PointSupport] = _cad_entity_list_property("PointSupports", "All the :any:`PointSupport` on this layer.")
    line_supports:  List[LineSupport]  = _cad_entity_list_property("LineSupports", "All the :any:`LineSupport` on this layer.")

    walls_below: List[Wall] = _cad_entity_list_property("WallsBelow", "All the :any:`Wall` below the slab on this layer.")
    walls_above: List[Wall] = _cad_entity_list_property("WallsAbove", "All the :any:`Wall` above the slab on this layer.")
    
    columns_below: List[Column] = _cad_entity_list_property("ColumnsBelow", "All the :any:`Column` below the slab on this layer.")
    columns_above: List[Column] = _cad_entity_list_property("ColumnsAbove", "All the :any:`Column` above the slab on this layer.")
    
    slab_areas: List[SlabArea] = _cad_entity_list_property("SlabAreas", "All the :any:`SlabArea` on this layer.")

    slab_openings: List[SlabOpening] = _cad_entity_list_property("SlabOpenings", "All the :any:`SlabOpening` on this layer.")

    beams: List[Beam] = _cad_entity_list_property("Beams", "All the :any:`Beam` on this layer.")

    # PUBLIC CAD ENTITY ADDITION METHODS

    def add_point_spring(self, location: Point2D) -> Column:
        """Add a :any:`PointSpring` at the given location, copying properties from :any:`CadManager.default_point_spring`.
                
        Note that the location will be snapped to the nearest 0.1mm"""
        return self._add_cad_entity_with_point("PointSpring", location)

    def add_line_spring(self, location: LineSegment2D) -> Wall:
        """Add a :any:`LineSpring` at the given location, copying properties from :any:`CadManager.default_line_spring`.
                
        Note that the location will be snapped to the nearest 0.1mm"""
        return self._add_cad_entity_with_line_segment("LineSpring", location)
    
    def add_area_spring(self, boundary: Polygon2D) -> AreaSpring:
        """Add a :any:`AreaSpring` at the given location, copying properties from :any:`CadManager.default_area_spring`.
                
        Note that the location will be snapped to the nearest 0.1mm"""
        return self._add_cad_entity_with_polygon("AreaSpring", boundary)
    
    def add_point_support(self, location: Point2D) -> Column:
        """Add a :any:`PointSupport` at the given location, copying properties from :any:`CadManager.default_point_support`.
                
        Note that the location will be snapped to the nearest 0.1mm"""
        return self._add_cad_entity_with_point("PointSupport", location)

    def add_line_support(self, location: LineSegment2D) -> Wall:
        """Add a :any:`LineSupport` at the given location, copying properties from :any:`CadManager.default_line_support`.
                
        Note that the location will be snapped to the nearest 0.1mm"""
        return self._add_cad_entity_with_line_segment("LineSupport", location)
    
    def add_beam(self, location: LineSegment2D) -> Wall:
        """Add a :any:`Beam` at the given location, copying properties from :any:`CadManager.default_beam`.
                
        Note that the location will be snapped to the nearest 0.1mm"""
        return self._add_cad_entity_with_line_segment("Beam", location)
    
    def add_column(self, location: Point2D) -> Column:
        """Add a :any:`Column` at the given location, copying properties from :any:`CadManager.default_column`.
                
        Note that the location will be snapped to the nearest 0.1mm"""
        return self._add_cad_entity_with_point("Column", location)

    def add_slab_area(self, location: Polygon2D) -> SlabArea:
        """Add a :any:`SlabArea` at the given location, copying properties from :any:`CadManager.default_slab_area`.
                
        Note that the location will be snapped to the nearest 0.1mm"""
        return self._add_cad_entity_with_polygon("SlabArea", location)
    
    def add_slab_opening(self, location: Polygon2D) -> SlabOpening:
        """Add a :any:`SlabOpening` at the given location, copying properties from :any:`CadManager.default_slab_opening`.
                
        Note that the location will be snapped to the nearest 0.1mm"""
        return self._add_cad_entity_with_polygon("SlabOpening", location)
    
    def add_wall(self, location: LineSegment2D) -> Wall:
        """Add a :any:`Wall` at the given location, copying properties from :any:`CadManager.default_wall`.
                
        Note that the location will be snapped to the nearest 0.1mm"""
        return self._add_cad_entity_with_line_segment("Wall", location)

