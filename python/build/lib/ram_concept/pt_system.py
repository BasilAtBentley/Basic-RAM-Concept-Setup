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
from .add_property import _no_none_data_property
from .add_property import _enum_string_property
from .add_property import _float_property
from .add_property import _int_property
from .add_property import _string_property
from .anchor_system import AnchorSystem
from .data import Data
from .duct_system import DuctSystem
from .duct_system import PTSystemType
from .strand_material import StrandMaterial

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class PTSystem(Data):
    """`PTSystem` represents a post-tensioning system.

    To create a new `PTSystem`, use :any:`PTSystems.add_pt_system`.
    To see all `PTSystems` that exist in a :any:`Model`, use :any:`PTSystems.pt_systems`.
    """
    # this class maps to Material + PTSystem  internally

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)
        

    # PUBLIC PROPERTIES

    # name inherited from Data
    # number inherited from Data, but not useful

    strand_material: StrandMaterial = _no_none_data_property("StrandMaterial",StrandMaterial,"The strand material in this PT system")
    anchor_system: AnchorSystem = _no_none_data_property("AnchorSystem",AnchorSystem,"The anchor system in this PT system")
    duct_system: DuctSystem = _no_none_data_property("DuctSystem",DuctSystem,"The duct system in this PT system")
    Fse: float   = _float_property("Fse", "Final effective stress of strand (not used if modeling `Jacks`)")

    # jack related properties
    long_term_losses: float = _float_property("LongTermLosses",  "Lump-sum long-term losses to use in calculating effective tendon stresses.")
    min_curvature_radius: float = _float_property("MinRadius",       "The minimum radius of curvature acceptable for this PT system.")

    # DEPRECATED PUBLIC PROPERTIES

    # properties relocated to strand material
    Aps = property(lambda self: self.strand_material.Aps, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`StrandMaterial.Aps` instead")
    Eps = property(lambda self: self.strand_material.Eps, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`StrandMaterial.Eps` instead")
    Fpu = property(lambda self: self.strand_material.Fpu, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`StrandMaterial.Fpu` instead")
    Fpy = property(lambda self: self.strand_material.Fpy, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`StrandMaterial.Fpy` instead")

    # properties relocated to anchor system
    jack_stress      = property(lambda self: self.anchor_system.jack_stress, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`AnchorSystem.jack_stress` instead")
    anchor_friction  = property(lambda self: self.anchor_system.anchor_friction, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`AnchorSystem.anchor_friction` instead")
    seating_distance = property(lambda self: self.anchor_system.seating_distance, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`AnchorSystem.seating_distance` instead")

    # properties relocated to duct system
    system_type      = property(lambda self: self.duct_system.system_type, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`DuctSystem.system_type` instead")
    duct_width       = property(lambda self: self.duct_system.duct_width, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`DuctSystem.duct_width` instead")
    strands_per_duct = property(lambda self: self.duct_system.strands_per_duct, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`DuctSystem.strands_per_duct` instead")
    wobble_friction  = property(lambda self: self.duct_system.wobble_friction, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`DuctSystem.wobble_friction` instead")
    angular_friction = property(lambda self: self.duct_system.angular_friction, None,None,"This property has been DEPRECATED but currently available as read-only. Use :any:`DuctSystem.angular_friction` instead")
    

    # PUBLIC OPERATIONS

    def delete(self) -> None:
        """Delete the `PTSystem` mix from the `Model`. The last `PTSystem` in a `Model` cannot be deleted."""
        if (len(self.model.pt_systems.pt_systems) == 1):
            raise Exception("Cannot delete last PTSystem in Model")

        self._delete()



    