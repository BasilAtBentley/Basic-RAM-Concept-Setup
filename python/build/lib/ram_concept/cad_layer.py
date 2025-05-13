#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import Any
from typing import List
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .cad_entity import CadEntity
    from .line_segment_2D import LineSegment2D
    from .model import Model
    from .point_2D import Point2D
    from .polygon_2D import Polygon2D

# -------------------------------------------------------------------------------------------------

class CadLayer(Data):
    """CadLayer represents a layer in the CAD system.
    
    `CadLayer` is abstract and is the superclass of all the layers in the CAD system.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    # Internally this encapsulates the behavior of both ACadLayer and CadLayer
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)
    
    # INTERNAL ENTITY ADDITION OPERATIONS

    def _add_cad_entity_with_line_segment(self, type:str, location: LineSegment2D) -> CadEntity:
        """Adds an entity of the given type at the given location."""

        return self._add_cad_entity(type, location.to_point_list_bracket_string())

    def _add_cad_entity_with_point(self, type:str, location: Point2D) -> CadEntity:
        """Adds an entity of the given type at the given location."""

        return self._add_cad_entity(type, location.to_point_list_bracket_string())

    def _add_cad_entity_with_polygon(self, type:str, boundary: Polygon2D) -> CadEntity:
        """Adds an entity of the given type at the given location."""

        return self._add_cad_entity(type, boundary.to_point_list_bracket_string())
        
    # INTERNAL ENTITY ADDITION OPERATIONS

    def _add_cad_entity(self, type: str, location: str) -> CadEntity:
        """Adds an entity of the given type at the given location (point list bracket string)."""

        cmd = "[NEW_ENTITY_USER][" + type + "]" + location
        uid = self._command(cmd)
        return self.model._get_data(uid)

    # EXISTING ENTITY ACCESS OPERATIONS

    def _get_entities(self, filter_key: str) -> List[CadEntity]:
        """Get a list of entities on this layer that corresponds to the given filter key."""
        cmd = "[GET_ENTITY_LIST][" + filter_key + "]"
        uids = self._command(cmd)
        return self.model._get_datas_from_bracket_string(uids)

    def _bulk_add(self,add_method_name: str, locations:List[Any]) -> List[CadEntity]:
        """Adds a set of `CadEntity` to this, using the given method name and locations.
        There is assumed to be a method with add_method_name, taking one argument that is the location."""
        # lambda methods could do this instead, but they couldn't handle the try/except logic

        # confirm that the method exists
        method = getattr(self, add_method_name)
        if method == None:
            raise Exception("Method {0} does not exist".format(add_method_name))
        
        # add and set
        entities = []

        try:
            for i_entity in range(0, len(locations)):
                entity = method(locations[i_entity])
                entities.append(entity)
        except Exception:
            # if creating any fails, we undo creation of all
            for entity in entities:
                entity.delete()
            raise

        return entities





