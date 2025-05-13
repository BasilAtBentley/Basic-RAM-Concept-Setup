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
    from .strand_material import StrandMaterial
    from .model import Model


# -------------------------------------------------------------------------------------------------

class StrandMaterials(Data):
    """`StrandMaterials` represents the collection of :any:`StrandMaterial` defined in the :any:`Model`.

    This is a singleton object which always exists in every :any:`Model`. It is available through :any:`Model.strand_materials`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by `Model`."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    strand_materials: List[StrandMaterial] = _data_child_list_property("StrandMaterial", "All of the :any:`StrandMaterial` in the `Model`")

    # CHILD ACCESS/CREATION OPERATIONS

    def add_strand_material(self, name: str) -> StrandMaterial:
        """Creates a new :any:`StrandMaterial` with the given name."""
        return self._add_unique_named_child("StrandMaterial", name)

    def strand_material(self, name: str) -> StrandMaterial:
        """Find the :any:`StrandMaterial` with the given name."""

        return self._get_named_child_of_type(name, "StrandMaterial")

