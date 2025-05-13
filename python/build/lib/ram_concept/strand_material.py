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
from .add_property import _float_property
from .add_property import _int_property
from .add_property import _string_property
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class StrandMaterial(Data):
    """`StrandMaterial` represents a strand in a post-tensioning system.

    To create a new `StrandMaterial`, use :any:`StrandMaterials.add_strand_material`.
    To see all `StrandMaterials` that exist in a :any:`Model`, use :any:`StrandMaterials.strand_materials`.
    """
    # this class maps to Material + StrandMaterial  internally

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""
        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    # name inherited from Data
    # number inherited from Data, but not useful

    Aps: float   = _float_property("Aps", "Area of strand")
    Eps: float   = _float_property("Eps", "Strand elastic modulus")
    Fpu: float   = _float_property("Fpu", "Ultimate tensile strength of strand")
    Fpy: float   = _float_property("Fpy", "Yield strength of strand")

    # PUBLIC OPERATIONS

    def delete(self) -> None:
        """Delete the `StrandMaterial` from the `Model`. The last `StrandMaterial` in a `Model` cannot be deleted."""
        if (len(self.model.strand_materials.strand_materials) == 1):
            raise Exception("Cannot delete last StrandMaterial in Model")

        self._delete()



    