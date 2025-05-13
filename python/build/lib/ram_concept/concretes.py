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
    from .concrete import Concrete
    from .model import Model


# -------------------------------------------------------------------------------------------------

class Concretes(Data):
    """`Concretes` represents the collection of :any:`Concrete` mixes defined in the :any:`Model`.

    This is a singleton object which always exists in every :any:`Model`. It is available through :any:`Model.concretes`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by `Model`."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    concretes: List[Concrete] = _data_child_list_property("Concrete", "All of the :any:`Concrete` mixes in the `Model`")

    # CHILD ACCESS/CREATION OPERATIONS

    def add_concrete(self, name: str) -> Concrete:
        """Creates a new :any:`Concrete` with the given name."""
        return self._add_unique_named_child("Concrete", name)

    def concrete(self, name: str) -> Concrete:
        """Find the :any:`Concrete` with the given name."""

        return self._get_named_child_of_type(name, "Concrete")

