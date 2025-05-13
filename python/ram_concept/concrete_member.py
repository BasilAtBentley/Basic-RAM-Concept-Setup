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
from .add_property import _no_none_data_property
from .cad_entity import CadEntity
from .concrete import Concrete

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class ConcreteMember(CadEntity):
    """ConcreteMember is an abstract superclass of concrete members.

    This class has 2 direct sublasses: :any:`ConcreteSpanningMember` and :any:`ConcreteSupport`
    
    ConcreteMembers are always located on the :any:`StructureLayer`.
    """
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    concrete: Concrete   = _no_none_data_property("ConcreteMix", Concrete, ":any:`Concrete` used by this `ConcreteMember`")

    # perhaps add IsmId later
