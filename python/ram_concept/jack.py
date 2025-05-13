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
from .add_property import _bool_property
from .add_property import _int_property
from .add_property import _enum_int_property
from .add_property import _float_property
from .add_property import _no_none_data_property
from .add_property import _point_location_property
from .add_property import _readonly_data_property
from .add_property import _readonly_float_property
from .cad_entity import CadEntity
from .enums import ElevationReference
from .point_2D import Point2D
from .tendon_node import TendonNode

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class Jack(CadEntity):
    """`Jack` is a post-tensioning jack at a :any:`TendonNode` (profile point).
    
    `Jacks` are always located on a :any:`TendonLayer`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PROPERTY PROPERTIES

    use_pt_system_defaults = _bool_property("UsePTSystemDefaults", "Use the PT System defaults for `Jack` properties instead of the ones defined in this `Jack`")

    anchor_friction  = _float_property("AnchorFriction",  "Friction coefficient for strands moving through the anchor.")
    long_term_losses = _float_property("LongTermLosses",  "Lump-sum long-term losses to use in calculating effective tendon stresses.")
    wobble_friction  = _float_property("WobbleFriction",  "Friction coefficient per unit length of tendon due to unintentional curvatures.")
    angular_friction = _float_property("AngularFriction", "Friction coefficient per angular change of tendon for use with intentional curvatures.")
    jack_stress      = _float_property("JackStress",      "Stress applied to the strands at the anchor by the this `Jack`.")
    seating_distance = _float_property("SeatingDistance", "Distance strands retract back into anchor while seating the wedges.")

    elongation = _readonly_float_property("Elongation", "Elongation of the tendon stressed by this Jack (only valid after calc-all).")

    node: TendonNode = _readonly_data_property("TendonNode0", "The `TendonNode` the `Jack` is connected to.")

    location : Point2D = _point_location_property("Read-only :any:`Point2D` location of this `Jack`.")

    # CONVENIENCE PROPERTY SETTING OPERATIONS

# -------------------------------------------------------------------------------------------------

class DefaultJack(Jack):
    """`DefaultJack` represents a `Jack` that stores the default values for future `Jacks` that are created.

    An `Exception` will be raised if the `location` or `node`  properties of `DefaultJack` are accessed.
    
    There is only 1 and always 1 `DefaultJack` in the `Model`. It is accessed through :any:`CadManager.default_jack`
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # CadEntity OVERRIDES

    def delete(self) -> None:
        """This method will raise an exception, as `delete` is not available for default objects."""
        raise Exception("delete() is not supported for default CadEntities")

