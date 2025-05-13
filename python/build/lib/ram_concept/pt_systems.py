#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import List
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .add_property import _data_child_list_property
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .pt_system import PTSystem
    from .model import Model


# -------------------------------------------------------------------------------------------------

class PTSystems(Data):
    """`PTSystems` represents the collection of :any:`PTSystem` defined in the :any:`Model`.

    This is a singleton object which always exists in every :any:`Model`. It is available through :any:`Model.pt_systems`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by `Model`."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    pt_systems: List[PTSystem] = _data_child_list_property("PTSystem", "All of the :any:`PTSystem` in the `Model`")

    # CHILD ACCESS/CREATION OPERATIONS

    def add_pt_system(self, name: str) -> PTSystem:
        """Creates a new :any:`PTSystem` with the given name."""

        ptSystem = self._add_unique_named_child("PTSystem", name)   
        
        #set strand, duct, and anchor of pt system to prevent null reference
        strand = self.model.strand_materials.strand_materials[0]
        duct = self.model.duct_systems.duct_systems[0]
        anchor = self.model.anchor_systems.anchor_systems[0]
        ptSystem.strand_material = strand
        ptSystem.duct_system = duct
        ptSystem.anchor_system = anchor

        return ptSystem


    def pt_system(self, name: str) -> PTSystem:
        """Find the :any:`PTSystem` with the given name."""

        return self._get_named_child_of_type(name, "PTSystem")

