#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .bracket_parser import BracketParser
from .data import Data
from .point_2D import Point2D
from .line_segment_2D import LineSegment2D
from .polygon_2D import Polygon2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class CadEntity(Data):
    """CadEntity represents an object in the CAD system.
    
    CadEntities always reside in a :any:`CadLayer`.
    CadEntity is be abstract and should only be subclassed by the Framework.
    """

    # Internally this can correspond to ACadNUEntity or ACadPUEntity (or ACadNode, currently)

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC OPERATIONS

    # this needs to be overridden whereever deletion is not available (read-only cases already covered)
    def delete(self) -> None:
        """Removes this `CadEntity` from the :any:`Model`."""
        if self._read_only:
            raise Exception("Cannot delete read-only CadEntity.")
        
        self._delete()

    # INTERNAL OPERATIONS

    def _get_location(self): # FUTURE add base class for geometry?
        """Gets the plan location of this cad entity.
        
        The class of the return value depends upon the cad entity type."""
        location_string = self._command("[GET_LOCATION_USER]")

        parser = BracketParser(location_string)

        # there should be 2 tokens, 1 for the type and the second for the data
        if(parser.count_remaining_tokens() != 2):
            raise Exception("Internal error: bad [GET_LOCATION_USER] return value: " + location_string)

        type_string = parser.next_token()
        data_string = parser.next_token()

        if type_string == "Point2D":
            return Point2D.from_bracket_string(data_string)
        elif type_string == "LineSeg2D":
            return LineSegment2D.from_bracket_string(data_string)
        elif type_string == "Polyline2D":
            raise Exception("Unsupported [GET_LOCATION_USER] geometry type: Polyline2D")
        elif type_string == "Polygon2D":
            return Polygon2D.from_bracket_string(data_string)
        elif type_string == "Rect2D":
            raise Exception("Unsupported [GET_LOCATION_USER] geometry type: Rect2D")
        elif type_string == "Compound2D":
            raise Exception("Unsupported [GET_LOCATION_USER] geometry type: Compound2D")
        elif type_string == "BoundaryShape2D":
            raise Exception("Unsupported [GET_LOCATION_USER] geometry type: BoundaryShape2D")
        elif type_string == "Circle":
            raise Exception("Unsupported [GET_LOCATION_USER] geometry type: Circle")
        else:
            raise Exception("Unknown [GET_LOCATION_USER] geometry type: " + type_string)




