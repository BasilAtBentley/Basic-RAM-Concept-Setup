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
from .add_property import _enum_string_property
from .add_property import _enum_int_property
from .add_property import _float_property
from .add_property import _int_property
from .add_property import _string_property
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class PTSystemType(Enum):
    """For specifying the bond-vs-unbonded type of a `PTSystem`.

    The available values are:

    * BONDED: the strands are bonded to the duct (and concrete) in service (after stressing).
    * UNBONDED: the strands are free to move longitudinally along the duct in service (after stressing).
    """
    BONDED    = "bonded"
    UNBONDED   = "unbonded"
    # EXTERNAL   = "external"

    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: str) -> PTSystemType:
        """Convert the internal value to the PTSystemType value (raise exception if invalid)."""
        return PTSystemType(internal_value) # will raise exception if invalid

    def _to_internal(self) -> str:
        """Convert the enum value into an internal integer."""
        return self.value

# -------------------------------------------------------------------------------------------------
class DuctShape(Enum):
    """For specifying the shape of the duct in `DuctSystem`.

    The available values are:

    * ROUND: the duct has a circular cross-section 
    * FLAT: the ducts has a narrow cross-section with two flat surfaces 
    * OVAL: the ducts has an oval cross-section
    """
    ROUND = 1
    FLAT = 2
    OVAL = 3
    
    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: int) -> DuctShape:
        """Convert the internal value to the DuctShape value (raise exception if invalid)."""
        return DuctShape(internal_value) # will raise exception if invalid

    def _to_internal(self) -> int:
        """Convert the enum value into an internal integer."""
        return self.value

# -------------------------------------------------------------------------------------------------
class DuctType(Enum):
    """For specifying the duct type of a `DuctSystem`.

    The available values are:

    * CORRUGATED_PLASTIC: the duct is made of PP or HDPE with corrugated or ribbed exterior surface to facilitate better bonding with the surrounding concrete.  
    * SMOOTH_PLASTIC: the duct is made of PP or HDPE with smooth non-corrugated surface.  
    * CORRUGATED_STEEL: the duct is made of steel (usually galvanized) with corrugated or ribbed exterior surface to facilitate better bonding with the surrounding concrete.  
    * SMOOTH_STEEL: the duct is made of steel (usually galvanized) with smooth non-corrugated surface. 
    * TIGHTLY_SHEATHED: is a tight radius duct or is coated with corrosion-inhibiting grease and protected with extruded sheathing
    """
    CORRUGATED_PLASTIC = 1
    SMOOTH_PLASTIC = 2
    CORRUGATED_STEEL = 3
    SMOOTH_STEEL = 4
    TIGHTLY_SHEATHED = 5

    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: int) -> DuctType:
        """Convert the internal value to the DuctType value (raise exception if invalid)."""
        return DuctType(internal_value) # will raise exception if invalid

    def _to_internal(self) -> int:
        """Convert the enum value into an internal integer."""
        return self.value

# -------------------------------------------------------------------------------------------------

class DuctSystem(Data):
    """`DuctSystem` represents a post-tensioning system.

    To create a new `DuctSystem`, use :any:`DuctSystems.add_duct_system`.
    To see all `DuctSystems` that exist in a :any:`Model`, use :any:`DuctSystems.duct_systems`.
    """
    # this class maps to Material + DuctSystem  internally

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""
        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    # name inherited from Data
    # number inherited from Data, but not useful
    system_type:      PTSystemType = _enum_string_property("PTSystemType", PTSystemType, "The type of PT System (bonded or unbonded).")
    duct_width:       float   = _float_property("DuctWidth", "Width of individual duct")
    strands_per_duct: float   = _float_property("StrandsPerDuct", "Maximum number of strands to place in a single duct")

    # jack related properties
    wobble_friction      = _float_property("WobbleFriction",  "Friction coefficient per unit length of tendon due to unintentional curvatures.")
    angular_friction     = _float_property("AngularFriction", "Friction coefficient per angular change of tendon for use with intentional curvatures.")

    # new properties added in 2023
    duct_height: float     = _float_property("DuctHeight", "Height of individual duct")
    duct_shape:  DuctShape = _enum_int_property("DuctShape",DuctShape,"Shape of Duct (round, flat or oval)")
    duct_type:   DuctType  = _enum_int_property("DuctType",DuctType,"Type of Duct (Corrugated plastic, smooth plastic, corrugated steel, smooth steel or tightly sheathed)")

    # PUBLIC OPERATIONS

    def delete(self) -> None:
        """Delete the `DuctSystem` mix from the `Model`. The last `DuctSystem` in a `Model` cannot be deleted."""
        if (len(self.model.duct_systems.duct_systems) == 1):
            raise Exception("Cannot delete last DuctSystem in Model")

        self._delete()



    