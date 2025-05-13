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
from .add_property import _cad_entity_list_copy_read_only_property
from .cad_layer import CadLayer
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .area_spring import AreaSpring
    from .elements import ColumnElement
    from .elements import WallElement
    from .elements import WallElementGroup
    from .elements import SlabElement
    from .model import Model
    from .line_segment_2D import LineSegment2D
    from .line_spring import LineSpring
    from .line_support import LineSupport
    from .point_spring import PointSpring
    from .point_support import PointSupport

# -------------------------------------------------------------------------------------------------

class ElementLayer(CadLayer):
    """`ElementLayer` represents the meshed structure, containing elements, supports and springs.
    
    The API does not provide any significant mechanisms the change the `ElementLayer` contents as
    they are intended to be generated through meshing.
    The `ElementLayer` is accessible through :any:`CadManager.element_layer`.
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)
        self._read_only = True

    # INTERNAL PROPERTY-RELATED OPERATIONS

    # PUBLIC PROPERTIES

    point_springs: List[PointSpring]  = _cad_entity_list_copy_read_only_property("PointSprings", "All the :any:`PointSpring` on this layer.")
    line_springs:  List[LineSpring]   = _cad_entity_list_copy_read_only_property("LineSprings", "All the :any:`LineSpring` on this layer.")
    area_springs:  List[AreaSpring]   = _cad_entity_list_copy_read_only_property("AreaSprings", "All the :any:`AreaSpring` on this layer.")

    point_supports: List[PointSupport] = _cad_entity_list_copy_read_only_property("PointSupports", "All the :any:`PointSupport` on this layer.")
    line_supports:  List[LineSupport]  = _cad_entity_list_copy_read_only_property("LineSupports", "All the :any:`LineSupport` on this layer.")

    wall_elements_below: List[WallElement] = _cad_entity_list_copy_read_only_property("WallElementsBelow", "All the :any:`WallElement` below the slab on this layer.")
    wall_elements_above: List[WallElement] = _cad_entity_list_copy_read_only_property("WallElementsAbove", "All the :any:`WallElement` above the slab on this layer.")
    
    column_elements_below: List[ColumnElement] = _cad_entity_list_copy_read_only_property("ColumnElementsBelow", "All the :any:`ColumnElement` below the slab on this layer.")
    column_elements_above: List[ColumnElement] = _cad_entity_list_copy_read_only_property("ColumnElementsAbove", "All the :any:`ColumnElement` above the slab on this layer.")
    
    slab_elements: List[SlabElement] = _cad_entity_list_copy_read_only_property("SlabElements", "All the :any:`SlabElement` on this layer.")

    wall_element_groups_below: List[WallElementGroup] = _cad_entity_list_copy_read_only_property("WallElementGroupsBelow", "All the :any:`WallElementGroup` below the slab on this layer.")
    wall_element_groups_above: List[WallElementGroup] = _cad_entity_list_copy_read_only_property("WallElementGroupsAbove", "All the :any:`WallElementGroup` above the slab on this layer.")
