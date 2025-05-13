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
from .add_property import _float_property
from .add_property import _int_property
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class CalcOptions(Data):
    """`CalcOptions` stores global calculation settings.
    
    There  is a single `CalcOptions` that is accessible through :any:`Model.calc_options`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    auto_xy_stabilize = _bool_property("AutoXYStabilize","Should the structure be automatically stabilized in the x- and y- directions.")

    create_viewable_self_dead_loading = _bool_property("CreateViewableSelfDeadLdg", "Should viewable loads be created on the self-dead loading layer?")

    zero_tension_interations = _int_property("ZeroTensionIterations", "The number of zero-tension iterations to use in zero-tension analysis.")

    zero_tension_accelerator_power = _float_property("ZeroTensionAcceleratorPower", "The exponent to use in determing the zero-tension accelerator factor.")

    zero_tension_max_acceleration = _float_property("ZeroTensionMaxAccelerator", "The maximum limiting value for the zero-tension accelerator factor.")

    supports_above_in_self_dead = _bool_property("SupportsAboveInSelfDead", "Should the weight of supports above be considered in the self-dead loading?")

    consider_tendon_component_in_punch_check_reaction = _bool_property("ConsiderTendonComponentInPunchCheckReaction", "Should the vertical component of the tendons be considered in punching shear calculations?")

    check_capacity_only = _bool_property("CheckCapacityOnly", "Should calculations be limited to checking capacity and not include design of reinforcement?")

    desired_element_size = _float_property("DesiredElementSize","Desired plan-dimension size for slab elements.")

    #FUTURE many more properties to add

    

    #FUTURE Child access operations (Ec2 annex)

