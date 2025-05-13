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
    from .duct_system import DuctSystem
    from .model import Model


# -------------------------------------------------------------------------------------------------

class DuctSystems(Data):
    """`DuctSystems` represents the collection of :any:`DuctSystem` defined in the :any:`Model`.

    This is a singleton object which always exists in every :any:`Model`. It is available through :any:`Model.duct_systems`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by `Model`."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    duct_systems: List[DuctSystem] = _data_child_list_property("DuctSystem", "All of the :any:`DuctSystem` in the `Model`")

    # CHILD ACCESS/CREATION OPERATIONS

    def add_duct_system(self, name: str) -> DuctSystem:
        """Creates a new :any:`DuctSystem` with the given name."""
        return self._add_unique_named_child("DuctSystem", name)

    def duct_system(self, name: str) -> DuctSystem:
        """Find the :any:`DuctSystem` with the given name."""

        return self._get_named_child_of_type(name, "DuctSystem")

