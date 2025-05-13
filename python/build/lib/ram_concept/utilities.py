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

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    pass

# -------------------------------------------------------------------------------------------------

# def can_be_float(value) -> bool:
#     """Determines if the value can be converted to a float with float(value)"""
#     try:
#         float(value)
#         return True
#     except ValueError:
#         return False

# -------------------------------------------------------------------------------------------------

def _raise_if_invalid_string_property_value(value: str) -> None:
    """Raises an exception if the given value is not valid for storing in a string property"""
    if "[" in value:
        raise Exception("String property values cannot contain '['.")

    if "]" in value:
        raise Exception("String property values cannot contain ']'.")

# -------------------------------------------------------------------------------------------------

def _user_str_to_API_float(value: str) -> float:
    """Converts from user-unit string to API-unit float."""
    # need to special case RAM Concept user values
    if value == "infinite":
        return float_info.max
    elif value == "-infinite":
        return -float_info.max

    return float(value)

def _API_float_to_user_str(value: float) -> str:
    """Converts from API-unit float to user-unit string."""
    # we need to accept all values that are convertable to float
    try:
        float_value = float(value)
    except:
        raise Exception("Not a valid float value: " + str(value))

    # need to special case RAM Concept user values
    if float_value == float_info.max:
        return "infinite"
    elif float_value == -float_info.max:
        return "-infinite"

    return str(float_value)

# -------------------------------------------------------------------------------------------------        

def _API_int_to_user_str(value: float) -> str:
    """Converts from API int to user string."""
    # we need to accept all values that are convertable to int
    try:
        int_value = int(value)
    except:
        raise Exception("Not a valid int value: " + str(value))

    return str(int_value)

# -------------------------------------------------------------------------------------------------

def _API_bool_to_user_str(value: float) -> str:
    """Converts from API bool to user string."""
    # we need to accept all values that are convertable to bool
    try:
        bool_value = bool(value)
    except:
        # don't believe this is ever reachable....anything can be converted to bool
        raise Exception("Not a valid bool value: " + str(value))

    return str(bool_value)
       
# -------------------------------------------------------------------------------------------------

def _bulk_set(entities:List[Any], property_name: str, values:List[Any]) -> None:
    """Sets the given property of the given entities to the given values.
    If values is None, no values are set, but no exception is raised."""
    if values == None:
        return
    
    if len(entities) != len(values):
        raise Exception("The number of entities and values to set must be equal.")

    for i_entity in range(0,len(entities)):
        entity = entities[i_entity]
        value = values[i_entity]
        setattr(entity, property_name, value)
