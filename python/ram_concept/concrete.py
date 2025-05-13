#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from sys import float_info
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .add_property import _bool_property
from .add_property import _bool_string_property
from .add_property import _data_property
from .add_property import _float_property
from .add_property import _int_property
from .add_property import _string_property
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class Concrete(Data):
    """`Concrete` represents a concrete mix.

    To create a new `Concrete`, use :any:`Concretes.add_concrete`.
    To see all `Concretes` that exist in a :any:`Model`, use :any:`Concretes.concretes`.
 
    One awkward part of dealing with Concrete properties is that they have to be consistent at all points in time:

     - fc_initial <= fc_final
     - fcu_initial <= fcu_final
     - user_Ec_initial < user_Ec_final

    Attempting to set a value that violates one of the above constraints will raise an exception.

    The cube and cylinder concrete strengths have an implied relationship between them. Setting the cube strength will also
    modify the related cylinder strength and vis-versa. This is typically of no concern as a :any:`Model` only uses one design code.
    """
    # this class maps to Data + Material internally

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)
    
    # PUBLIC CONSTANTS

    USE_UNIT_MASS_INSTEAD = float_info.max
    """A flag value for `unit_mass_for_loads` to indicate that the `unit_mass` value should be considered for load calculations."""

    # PUBLIC PROPERTIES

    # name inherited from Data
    # number inherited from Data, but not useful

    coefficient_of_thermal_expansion: float = _float_property("CoefficientOfThermalExpansion", "Coefficient of thermal expansion")

    fc_initial: float = _float_property("FcInitial", "Early age concrete cylinder strength")
    fc_final: float   = _float_property("FcFinal",   "Final concrete cylinder strength")

    fcu_initial: float = _float_property("FcuInitial", "Early age concrete cube strength")
    fcu_final: float = _float_property("FcuFinal", "Final concrete cube strength")

    poissons_ratio: float = _float_property("PoissonsRatio", "Poisson's ratio")

    unit_mass: float = _float_property("UnitWeight", "Concrete density (mass/volume)")
    unit_unit_mass_for_loads: float = _float_property("UnitWeightForLoads", "Concrete density (mass/volume) for self-weight calculations (USE_UNIT_MASS_INSTEAD is flag value for 'use `unit_mass` instead')")

    user_Ec_initial: float = _float_property("UserEcInitial", "Early age concrete modulus of elasticity, when not calculating that value per code")
    user_Ec_final: float = _float_property("UserEcFinal", "Final concrete modulus of elasticity, when not calculating that value per code")

    use_code_Ec: float =_bool_string_property("EcCalc", "Code", "UserEc", "Code calculated values used instead of user_Ec_initial and user_Ec_final.")

    # PUBLIC OPERATIONS

    def delete(self) -> None:
        """Delete the concrete mix from the Model. The last concrete mix in a Model cannot be deleted."""
        if (len(self.model.concretes.concretes) == 1):
            raise Exception("Cannot delete last Concrete in Model")

        self._delete()



    