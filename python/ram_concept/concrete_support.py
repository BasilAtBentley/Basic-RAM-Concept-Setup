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
from .add_property import _bool_string_property
from .add_property import _int_property
from .add_property import _float_property
from .add_property import _string_property
from .concrete_member import ConcreteMember

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class ConcreteSupport(ConcreteMember):
    """`ConcreteSupport` is an abstract superclass of for :any:`Wall` and :any:`Column`.
    
    `ConcreteSupports` are always located on the :any:`StructureLayer`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    fixed_near = _bool_property("FixedNear", "Rotational fixity of the support to the slab")

    fixed_far = _bool_property("FixedFar", "Rotational fixity of the support at the end away from the slab")

    compressible = _bool_property("Compressible", "Is the support compressible? (if False, the support is infinitely rigid vertically)")

    height = _float_property("Height", "Vertical dimension of the support")

    below_slab = _bool_string_property("SupportSet", "below", "above", "Is this support below the slab? (above the slab if false)")

    use_specified_LLR_parameters = _bool_property("UseSpecifiedLlrParameters", "Use the specified live load reduction parameters instead of the calculated ones (use the calculated ones if false).")

    specified_LLR_levels = _int_property("SpecifiedLlrLevels", "The user specified number of levels being supported (for live load reduction calculation purposes")

    specified_trib_area = _float_property("SpecifiedTribArea", "The user specified tributary area being supported (for live load reduction calculation purposes, if the live load reduction code uses tributary area)")

    specified_influence_area = _float_property("SpecifiedInfluenceArea", "The user specified influences area being supported (for live load reduction calculation purposes, if the live load reduction code uses influence area)")

    llr_max_reduction = _float_property("LlrMaxReduction", "The maximum allowed (by user) live load reduction percentage for this support (0->100).")
