#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from enum import Enum
from typing import List
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .point_2D import Point2D
from .line_segment_2D import LineSegment2D
from .polygon_2D import Polygon2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .cad_entity import CadEntity

# -------------------------------------------------------------------------------------------------

# This file contains property constructing methods that are relevant for Data classes.

# -------------------------------------------------------------------------------------------------
# PROPERTIES THAT ARE POTENTIALLY RELEVANT FOR ALL DATA
# -------------------------------------------------------------------------------------------------

def _string_property(name: str, doc: str) -> property:
    """Adds a standard Data property access for the string property with the given name."""
    def getter(self) -> str:
        return self._get_string_property(name)
    def setter(self, value: str):
        self._set_property_raise_if_read_only()
        self._set_string_property(name,value)
    
    return property(getter,setter,None, "str: " + doc)

# -------------------------------------------------------------------------------------------------

def _float_property(name: str, doc: str) -> property:
    """Adds a standard Data property access for the float property with the given name."""
    def getter(self) -> float:
        return self._get_float_property(name)
    def setter(self, value: float):
        self._set_property_raise_if_read_only()
        self._set_float_property(name,value)
    
    return property(getter,setter,None, "float: " + doc)

def _readonly_float_property(name: str, doc: str) -> property:
    """Adds a standard Data property access for the float property with the given name."""
    def getter(self) -> float:
        return self._get_float_property(name)
    
    return property(getter,None,None, "float: " + doc)

# -------------------------------------------------------------------------------------------------

def _int_property(name: str, doc: str) -> property:
    """Adds a standard Data property access for the int property with the given name."""
    def getter(self) -> int:
        return self._get_int_property(name)
    def setter(self, value: int):
        self._set_property_raise_if_read_only()
        self._set_int_property(name,value)
    
    return property(getter,setter,None,"int: " + doc)

def _readonly_int_property(name: str, doc: str) -> property:
    """Adds a read-only standard Data property access for the int property with the given name."""
    def getter(self) -> int:
        return self._get_int_property(name)
    
    return property(getter,None,None,"int: " + doc)

# -------------------------------------------------------------------------------------------------

def _bool_property(name: str, doc: str) -> property:
    """Adds a standard Data property access for the bool property with the given name."""
    def getter(self) -> bool:
        return self._get_bool_property(name)
    def setter(self, value: bool):
        self._set_property_raise_if_read_only()
        self._set_bool_property(name,value)
    
    return property(getter,setter,None,"bool: " + doc)

def _readonly_bool_property(name: str, doc: str) -> property:
    """Adds a standard Data property access for the read-only bool property with the given name."""
    def getter(self) -> bool:
        return self._get_bool_property(name)
    
    return property(getter,None,None,"bool: " + doc)

# -------------------------------------------------------------------------------------------------

def _bool_string_property(name: str, true_value: str, false_value: str, doc: str) -> property:
    """Adds a bool property backed by a standard Data property access string with the given name.
    The given 'true_value' maps to True and the given 'false_value' maps to False."""
    def getter(self) -> bool:
        string_value = self._get_string_property(name)
        if string_value == true_value:
            return True
        elif string_value == false_value:
            return False
        else:
            raise Exception("Internal Error: unexpected value in " + name + " property: " + string_value)
    def setter(self, value: bool):
        self._set_property_raise_if_read_only()
        try:
            bool_value = bool(value)
        except:
            raise Exception(name + " property requires bool values.") # don't think this is possible...everything converts to bool

        if bool_value:
            self._set_string_property(name,true_value)
        else:
            self._set_string_property(name,false_value)
    
    return property(getter,setter,None,"bool: " + doc)

def _readonly_bool_string_property(name: str, true_value: str, false_value: str, doc: str) -> property:
    """Adds a read-only bool property backed by a standard Data property access string with the given name.
    The given 'true_value' maps to True and the given 'false_value' maps to False."""
    def getter(self) -> bool:
        string_value = self._get_string_property(name)
        if string_value == true_value:
            return True
        elif string_value == false_value:
            return False
        else:
            raise Exception("Internal Error: unexpected value in " + name + " property: " + string_value)
    
    return property(getter,None,None,"bool: " + doc)

# -------------------------------------------------------------------------------------------------

def _data_property(name: str, required_class, doc: str) -> property:
    """Adds a standard Data property access for the Data property with the given name."""
    def getter(self): #-> Data:
        return self._get_data_property(name)
    def setter(self, value):
        self._set_property_raise_if_read_only()

        self._set_data_property(name,required_class, value)
    
    return property(getter,setter,None,doc)

def _readonly_data_property(name: str, doc: str) -> property:
    """Adds a standard read-only Data property access for the Data property with the given name."""
    def getter(self): #-> Data:
        return self._get_data_property(name)
    
    return property(getter,None,None,doc)

# -------------------------------------------------------------------------------------------------

def _no_none_data_property(name: str, required_class, doc: str) -> property:
    """Adds a standard Data property access for the None-not-allowed Data property with the given name."""
    def getter(self): #-> Data:
        return self._get_data_property(name)

    def setter(self, value):
        self._set_property_raise_if_read_only()

        if value is None:
            raise Exception("None is not a valid value for this property")

        self._set_data_property(name, required_class, value)
    
    return property(getter,setter,None,doc)

def _key_data_property(key: str, doc: str) -> property:
    """Adds a standard property access to a Data that can be found with a keystring."""
    def getter(self): #-> Data:
        return self.model._get_data_from_key(key)
    
    return property(getter,None,None,doc)

# -------------------------------------------------------------------------------------------------

def _data_child_list_property(child_type: str, doc: str) -> property:
    """Adds a standard property access to a list of children of the given type."""
    def getter(self): #-> Data:
        return self._get_children_of_type(child_type)
    
    return property(getter,None,None,doc)

# -------------------------------------------------------------------------------------------------

# PROPERTIES WITH A STRING-ENUM MAPPING
# Requires the Enum to have 2 static methods
#   - _to_internal(self)
#   - _to_API(cls, internal_value)

def _enum_string_property(name: str, enum_class: Enum,  doc: str) -> property:
    """Adds a enum property backed by a standard Data property access string with the given name."""
    def getter(self) -> bool:
        internal_value = self._get_string_property(name)
        return enum_class._to_API(internal_value) # will raise exception for bad values (which are NOT expected)

    def setter(self, value: Enum):
        self._set_property_raise_if_read_only()
        internal_value = enum_class._to_internal(value)
        self._set_string_property(name,internal_value)
    
    return property(getter,setter,None, doc)

def _readonly_enum_string_property(name: str, enum_class: Enum,  doc: str) -> property:
    """Adds a enum property backed by a standard Data property access string with the given name."""
    def getter(self) -> bool:
        internal_value = self._get_string_property(name)
        return enum_class._to_API(internal_value) # will raise exception for bad values (which are NOT expected)
    
    return property(getter,None,None, doc)


# -------------------------------------------------------------------------------------------------

# PROPERTIES WITH A int-ENUM MAPPING
# Requires the Enum to have 2 static methods
#   - _to_internal(self)
#   - _to_API(cls, internal_value)

def _enum_int_property(name: str, enum_class: Enum,  doc: str) -> property:
    """Adds a enum property backed by a standard Data property access int with the given name."""
    def getter(self) -> bool:
        internal_value = self._get_int_property(name)
        return enum_class._to_API(internal_value) # will raise exception for bad values (which are NOT expected)

    def setter(self, value: Enum):
        self._set_property_raise_if_read_only()
        internal_value = enum_class._to_internal(value)
        self._set_int_property(name,internal_value)
    
    return property(getter,setter,None, doc)

def _readonly_enum_int_property(name: str, enum_class: Enum,  doc: str) -> property:
    """Adds a read-only enum property backed by a standard Data property access int with the given name."""
    def getter(self) -> bool:
        internal_value = self._get_int_property(name)
        return enum_class._to_API(internal_value) # will raise exception for bad values (which are NOT expected)
    
    return property(getter,None,None, doc)


# -------------------------------------------------------------------------------------------------
# PROPERTIES THAT ARE POTENTIALLY RELEVANT FOR ALL CAD LAYERS
# -------------------------------------------------------------------------------------------------

def _cad_entity_list_property(filter_key: str, doc: str) -> property:
    """Adds a read-only standard CadLayer property access to the CadEntities associated with the given filter key."""
    def getter(self) -> List[CadEntity]:
        return self._get_entities(filter_key)
    
    return property(getter,None,None,doc)

def _cad_entity_list_copy_read_only_property(filter_key: str, doc: str) -> property:
    """Adds a read-only standard CadLayer property access to the CadEntities associated with the given filter key
    AND it sets the readonly flag to match that of the layer it is contained in"""
    def getter(self) -> List[CadEntity]:
        entities = self._get_entities(filter_key)
        
        for entity in entities:
            entity._read_only = self._read_only
        return entities
    
    return property(getter,None,None,doc)


# -------------------------------------------------------------------------------------------------
# PROPERTIES THAT ARE POTENTIALLY RELEVANT FOR ALL CAD ENTITIES
# -------------------------------------------------------------------------------------------------

def _point_property(name: str, doc: str) -> property:
    """Adds a standard Data property access for the Point2D property with the given name."""
    def getter(self) -> Point2D:
        return self._get_point2D_property(name)
    def setter(self, value: Point2D):
        self._set_point2D_property(name,value)
    
    return property(getter,setter,None, "Point2D: " + doc)

def _point_location_property(doc: str) -> property:
    """Creates a CadEntity property that returns a point location."""
    def getter(self): #-> Point2D:
        point: Point2D = self._get_location()
        return point
    
    return property(getter,None,None,"Point2D: " + doc)

def _line_segment_location_property(doc: str) -> property:
    """Creates a CadEntity property that returns a line segment location."""
    def getter(self): #-> LineSegment2D:
        line_segment: LineSegment2D = self._get_location()
        return line_segment
    
    return property(getter,None,None,"LineSegment2D: " + doc)

def _polygon_location_property(doc: str) -> property:
    """Creates a CadEntity property that returns a polygon location."""
    def getter(self): #-> Polygon2D:
        polygon: Polygon2D = self._get_location()
        return polygon
    
    return property(getter,None,None,"Polygon2D: " + doc)

# -------------------------------------------------------------------------------------------------

# PROPERTIES THAT ARE RELEVANT ONLY FOR CadManager

def _cad_default_property(cad_entity_type: str, doc: str) -> property:
    """Creates a CadManager property that returns the appropriate default object for the given entity type."""
    def getter(self): #-> DefaultXxx
        command = "[GET_DEFAULT_OBJECT_FOR][" + cad_entity_type + "]"
        return self.model._get_data(self._command(command))
    
    return property(getter,None,None,doc)

# -------------------------------------------------------------------------------------------------

# PROPERTIES THAT ARE RELEVANT ONLY FOR ConcreteSpanningMember

def _stiffness_property(name: str, doc: str) -> property:
    """Creates a ConcreteSpanningMember property for custom stiffness factors."""
    def getter(self): #-> DefaultXxx
        # can always get the values
        return self._get_float_property(name)
    def setter(self, value: float):
        self._set_property_raise_if_read_only()
        if self._has_custom_stiffness_behavior():
            self._set_float_property(name,value)
        else:
            raise Exception("Cannot set stiffness factors unless the behavior is custom.")
    
    return property(getter,setter,None,"float: " + doc)




