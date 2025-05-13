#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from enum import Enum
from sys import float_info
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .add_property import _bool_property
from .add_property import _bool_string_property
from .add_property import _data_property
from .add_property import _enum_int_property
from .add_property import _float_property
from .add_property import _int_property
from .add_property import _string_property
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class AnchorType(Enum):
    """For specifying the anchor type of an `AnchorSystem`.

    The available values are:

    * MONOSTRAND: the basic anchorage system used for single-strand tendons,
    * FLAT_MULTI_PLANE: the anchorage system has rectangular plate with multiple plane bearing surfaces,
    * FLAT_SINGLE_PLANE: the anchorage system has rectangular plate with single plane bearing surface,
    * CIRCULAR_MULTI_PLANE: the anchorage system has circular plate with multiple plane bearing surfaces,
    * CIRCULAR_SINGLE_PLANE: = the anchorage system has circular plate with single plane bearing surface,
    * SQUARE_MULTI_PLANE: = the anchorage system has square plate with multiple plane bearing surfaces,
    * SQUARE_SINGLE_PLANE: = the anchorage system has square plate with single plane bearing surface
    """
    MONOSTRAND = 1
    FLAT_MULTI_PLANE = 2
    FLAT_SINGLE_PLANE = 3
    CIRCULAR_MULTI_PLANE = 4
    CIRCULAR_SINGLE_PLANE = 5
    SQUARE_MULTI_PLANE = 6
    SQUARE_SINGLE_PLANE = 7

    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: int) -> AnchorType:
        """Convert the internal value to the AnchorType value (raise exception if invalid)."""
        return AnchorType(internal_value) # will raise exception if invalid

    def _to_internal(self) -> int:
        """Convert the enum value into an internal integer."""
        return self.value

# -------------------------------------------------------------------------------------------------

class AnchorSystem(Data):
    """`AnchorSystem` represents an anchoring system in a post-tensioning system.

    To create a new `AnchorSystem`, use :any:`AnchorSystems.add_anchor_system`.
    To see all `AnchorSystems` that exist in a :any:`Model`, use :any:`AnchorSystems.anchor_systems`.
    """
    # this class maps to Material + AnchorSystem  internally

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""
        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    # name inherited from Data
    # number inherited from Data, but not useful
    
    anchor_type:      AnchorType  = _enum_int_property("AnchorType",AnchorType,"Type of anchorage device used to transfer tendon forces to the concrete")
    jack_stress:      float       = _float_property("JackStress",      "Stress applied to strands at the anchor by the the `Jack`.")
    seating_distance: float       = _float_property("SeatingDistance", "Distance strands retract back into anchor while seating the wedges.")
    anchor_friction:  float       = _float_property("AnchorFriction",  "Friction coefficient for strands moving through the anchor.")
    
    # PUBLIC OPERATIONS

    def delete(self) -> None:
        """Delete the `AnchorSystem` from the `Model`. The last `AnchorSystem` in a `Model` cannot be deleted."""
        if (len(self.model.anchor_systems.anchor_systems) == 1):
            raise Exception("Cannot delete last AnchorSystem in Model")

        self._delete()



    