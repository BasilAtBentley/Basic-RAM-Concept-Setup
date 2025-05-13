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
    from .anchor_system import AnchorSystem
    from .model import Model


# -------------------------------------------------------------------------------------------------

class AnchorSystems(Data):
    """`AnchorSystems` represents the collection of :any:`AnchorSystem` defined in the :any:`Model`.

    This is a singleton object which always exists in every :any:`Model`. It is available through :any:`Model.anchor_systems`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by `Model`."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    anchor_systems: List[AnchorSystem] = _data_child_list_property("AnchorSystem", "All of the :any:`AnchorSystem` in the `Model`")

    # CHILD ACCESS/CREATION OPERATIONS

    def add_anchor_system(self, name: str) -> AnchorSystem:
        """Creates a new :any:`AnchorSystem` with the given name."""
        return self._add_unique_named_child("AnchorSystem", name)

    def anchor_system(self, name: str) -> AnchorSystem:
        """Find the :any:`AnchorSystem` with the given name."""

        return self._get_named_child_of_type(name, "AnchorSystem")

