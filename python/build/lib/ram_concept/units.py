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
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class Units(Data):
    """Units represents the singleton Units objects in a :any:`Model`, which controls the user unit system.
    
    The API operates using the same unit system as the RAM Concept UI. The methods in this class
    affect both the UI and the API. Generally you will want to:

    - Call :any:`get_units` after opening the file, and store the return value.
    - Call either :any:`set_US_API_units` or :any:`set_SI_API_units` to select the unit system that you want the API to use.
    - Call :any:`set_units` before closing (and saving) the file to restore the units to their original state.

    For newly created files, you will want to call one of these methods to ensure the users see a reasonable set of units:

    - :any:`set_US_user_units`
    - :any:`set_SI_user_units`
    - :any:`set_MKS_user_units`
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC OPERATIONS

    def set_US_user_units(self) -> None:
        """Set the unit system to be a reasonable default for projects using customary US units."""
        self._command("[RESET_UNITS][us]")        

    def set_SI_user_units(self) -> None:
        """Set the unit system to be a reasonable default for projects using SI units."""
        self._command("[RESET_UNITS][si]")        

    def set_MKS_user_units(self) -> None:
        """Set the unit system to be a reasonable default for projects using MKS units."""
        self._command("[RESET_UNITS][MKS]")        

    def set_US_API_units(self) -> None:
        """Set the unit system to be a predictable set of US units.

        - All lengths are inches.
        - All angles are degrees.
        - All forces are pounds.
        - All masses are pounds.
        - All time is seconds.
        - All temperatures are Fahrenheit.

        This leads to all areas being in square inches, all stresses being in psi, etc..
        """
        self._command("[RESET_UNITS][us_api]")        

    def set_SI_API_units(self) -> None:
        """Set the unit system to be a predictable set of SI units.

        - All lengths are meters.
        - All angles are degrees.
        - All forces are Newtons.
        - All masses are kilograms.
        - All time is seconds.
        - All temperatures are Celsius.

        This leads to all areas being in square meters, all stresses being in Pascals, etc..
        """
        self._command("[RESET_UNITS][si_api]")        


    def get_units(self) -> str:
        """Returns the current unit settings that affect both the API and the UI.

        The return value for this is only intended for use in the :any:`set_units` method.
        The `get_units`/`set_units` pair allow you to restore the units in file after modifying them.
        """
        return self._command("[GET_UNITS]")

    def set_units(self, unit_settings: str) -> None:
        """Restores the unit settings to the given value, which is required to have been returned from :any:`get_units`."""

        self._command("[SET_UNITS][" + unit_settings + "]")