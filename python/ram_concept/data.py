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
from .bracket_parser import BracketParser
from .add_property import _string_property, _readonly_int_property
from .point_2D import Point2D
from .point_3D import Point3D
from .utilities import _API_bool_to_user_str
from .utilities import _API_float_to_user_str
from .utilities import _API_int_to_user_str
from .utilities import _user_str_to_API_float
from .utilities import _raise_if_invalid_string_property_value


# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class _PropertyUnits(Enum):
    """For internal use only."""
    Internal = 1
    User = 2

# -------------------------------------------------------------------------------------------------

# *** NOTES on Read-Only and Delete ***
#
# The API needs to protect the client programmer, making data-corrupting operations difficult if not impossible. The primary
# strategy to achieve that is to not expose those corrupting operations (or make them only exposed via "private" underscore 
# attributes and methods). However, sometimes that alone is not enough, for example:
#
#   - Some loads are read-only and some are not (the generated ones are read-only)
#   - Some LoadingLayers can have loads added, and some can not
#   - CadEntities can be deleted, except for Default CadEntities
#
# Note that there is no direct correlation between read-only and not-deletable. For example, cad Default* are not deletable,
# but they are read-write.
#
# The general approach taken is to deal with this is:
#
#   - All Data has a _read_only flag attribute
#       - By default the _read_only flag is false
#       - Subclasses that need it, set it in the constructor or have other special logic to set it.
#   - The _read_only attribute is checked whenever setting properties (raising an exception if the Data is read-only
#   - delete() is only exposed in limited branches of the class hierarchy
#       - delete() is overridden in subclasses where delete() is forbidden (raising an exception)
#       - sometimes (such as in CadLayer) special logic is used
#   

class Data:
    """Data represents a significant data object in a :any:`Model`.

    Direct use of this class (instead of a more-specific subclass) is likely an error.
    
    This class should only be subclassed by the framework."""
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = [
        "_model",
        "_read_only",
         "_uid"
    ]

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by `Model`."""
        assert type(uid) is int # want to prevent str from slipping in
        super().__init__()
        self._uid = uid
        self._model = model
        self._read_only = False

    # INTERNAL PROPERTY HELPERS

    def _get_number(self)->int:
        """Gets the 1-based number of this Data, matching what would appear in the RAM Concept UI."""
        return self._get_int_property("Number") + 1

    # PUBLIC PROPERTY ACCESS OPERATIONS

    model: Model = property(lambda self: self._model, None, None, "The :any:`Model` that contains this :any:`Data`.")

    uid: int = property(lambda self: self._uid, None, None,"int: Read-only UID of this :any:`Data`")

    name = _string_property("Name", "Name of this :any:`Data` (note that name is not relevant in all `Data` subclasses)")

    number : int = property(_get_number, None, None, "1-based Number of this :any:`Data` (note that number is not relevant in all `Data` subclasses)")

    # PYTHON EQUALITY OPERATIONS

    def __eq__(self,obj):
        """Equals operation for Data objects"""
        if (obj.__class__ == self.__class__):
            return (self._uid == obj._uid) and (self._model == obj._model)
        else:
            return False

    # SUPPORT FOR READ-ONLY

    def _class_name(self) -> str:
        """Return the name of this class (intended mostly for error messages)."""
        return type(self).__name__

    def _set_property_raise_if_read_only(self) -> None:
        """Raises and exception with a property-related message if this Data is read-only."""
        if self._read_only:
            raise Exception("Cannot set properties of read-only " + self._class_name() + ".")

    def _operation_raise_if_read_only(self, operation: str) -> None:
        """Raises and exception with a operation-related message (cannot X with read-only Y) if this Data is read-only."""
        if self._read_only:
            raise Exception("Cannot " + operation + "with read-only " + self._class_name() + ".")

    # SUPPORT FOR UNIQUE NAMES

    def _raise_if_not_valid_unique_child_name(self, name: str) -> None:
        """Determine if the given name is a reasonable unique name, and is unique among the children."""
        # exclude None
        if name == None:
            raise Exception("Name cannot be 'None'.")

        # exclude empty
        if name == "":
            raise Exception("Name must be provided.")

        # check name validity
        _raise_if_invalid_string_property_value(name)

        # check that no child has same name
        children = self._get_children()
        for child in children:
            if child.name == name:
                raise Exception("Unique value must be provided for Name.")


    # CORE COMMAND OPERATION

    def _command(self, cmd: str) -> str:
        """Runs the given command in the context of this Data ("WITH_TARGET")."""

        full_command = "[WITH_TARGET][" + str(self.uid) + "][" + cmd + "]"
        return self.model._command(full_command)

    # DELETION OPERATIONS

    def _delete(self) -> None:
        """Delete this `Data` from the `Model`.

        THIS IS A DANGEROUS OPERATION THAT CAN CORRUPT THE MODEL.
        Only use delete() operations (no underscore)."""
        self._command("[DELETE]")

    # CHILD ACCESS OPERATIONS

    def _add_unique_named_child(self, type: str, name: str) -> Data:
        """Add and return a child Data with the given type and name, after ensuring the name is unique across all children.
        
        This validates the name for uniqueness and ensures no invalid characters.
        """
        self._raise_if_not_valid_unique_child_name(name)

        # if we get here, we can create the child
        command = "[ADD_CHILD][" + type + "][" + name + "][NO_SORT]"
        uid = self._command(command)
        return self.model._get_data(uid)

    # CHILD ACCESS OPERATIONS

    def _get_children(self) -> List[Data]:
        """Returns all the child Datas of this Data."""

        return_value = self._command("[GET_CHILDREN]") 
        tokens :List[str] = BracketParser.parse(return_value)
        return self.model._get_datas(tokens)

    def _get_children_of_type(self, type: str) -> List[Data]:
        """Returns all children of this Data with the exact matching type (subclasses not included)."""

        cmd = "[GET_CHILDREN_OF_TYPE][" + type + "]"
        uids = self._command(cmd)
        return self.model._get_datas_from_bracket_string(uids)

    def _get_only_child_of_type(self, type: str) -> Data:
        """Returns the only child of this Data with the given type.

        Throws an exception if there are no children or more than 1 child.
        """

        children: List[Data] = self._get_children_of_type(type)
        if(len(children) < 1):
            raise Exception("No children of type '" + type + "' exist.")
        elif(len(children) > 1):
            raise  Exception("More than 1 child of type '" + type + "' exists.")
        else:
            return children[0]

    def _get_named_child_of_type(self, name: str, type: str) -> Data:
        """Returns the child of the given type and name."""

        cmd = "[GET_NAMED_CHILD][" + name + "][" + type + "]"
        uid = self._command(cmd)
        if (uid == ""):
            return None
        return self.model._get_data(uid)

    def _get_named_child(self, name: str) -> Data:
        """Returns the child with the given name."""

        cmd = "[GET_NAMED_CHILD][" + name + "][ANY]"
        uid = self._command(cmd)
        return self.model._get_data(uid)

    # GENERIC PROPERTY ACCESS OPERATIONS

    # def get_property_names(self) -> str[]:

    # string property access

    def _get_string_property(self, property_name: str) -> str:
        """Gets the value of the (string) property with the given name."""

        return self._get_property(property_name, _PropertyUnits.Internal)

    def _set_string_property(self, property_name: str, value: str) -> None:
        """Sets the property with the given name to the given value."""

        self._set_property(property_name, value, _PropertyUnits.Internal) 

    # float property access
    
    def _get_float_property(self, property_name: str) -> float:
        """Gets the value of the (float) property with the given name."""

        float_string = self._get_property(property_name, _PropertyUnits.User)

        # need to special case RAM Concept user values
        return _user_str_to_API_float(float_string)

    def _set_float_property(self, property_name: str, value: float) -> None:
        """Sets the named property to the given value."""
        float_string = _API_float_to_user_str(value) # may raise exception

        self._set_property(property_name, float_string, _PropertyUnits.User)

    # int property access

    def _get_int_property(self, property_name: str) -> int:
        """Gets the value of the (int) property with the given name."""

        int_string = self._get_property(property_name, _PropertyUnits.Internal)
        return int(int_string)

    def _set_int_property(self, property_name: str, value: int) -> None:
        """Sets the named property to the given value."""

        int_string = _API_int_to_user_str(value) # may raise exception

        self._set_property(property_name, int_string, _PropertyUnits.Internal)

    # bool property access

    def _get_bool_property(self, property_name: str) -> bool:
        """Gets the value of the (bool) property with the given name."""

        bool_string = self._get_property(property_name, _PropertyUnits.Internal)
        lc_bool_string = bool_string.lower()

        if(lc_bool_string == "true"):
            return True
        elif (lc_bool_string == "false"):
            return False
        else:
            raise Exception("Unexpected bool string: " + bool_string)

    def _set_bool_property(self, property_name: str, value: bool) -> None:
        """Sets the named property to the given value."""

        bool_string = _API_bool_to_user_str(value) # may raise exception

        self._set_property(property_name, bool_string, _PropertyUnits.Internal)

    # data property access

    def _get_data_property(self, property_name: str) -> Data:
        """Gets the value of the (Data) property with the given name."""

        uid_string = self._get_property(property_name, _PropertyUnits.Internal)
        if(uid_string == ""):
            return None

        return self.model._get_data(uid_string)
        
    def _set_data_property(self, property_name: str, required_class, value: Data) -> None:
        """Sets the named property to the given (Data) value."""

        uid = "0" # 0 will be used in None case

        if not (value is None):
            if not isinstance(value, required_class):
                raise Exception("Attempting to set wrong type in " + str(required_class) + " property: " + str(value))

            if (value.model != self.model):
                raise Exception("Attempting to set property of Data in one model to reference of Data in another Model.")

            uid = str(value.uid)

        self._set_property(property_name, uid, _PropertyUnits.Internal)

    # Point2D property access
    
    def _get_point2D_property(self, property_name: str) -> Point2D:
        """Gets the value of the (Point2D) property with the given name."""

        point_string = self._get_property(property_name, _PropertyUnits.User)

        return Point2D.from_bracket_string(point_string)

    def _set_point2D_property(self, property_name: str, value: Point2D) -> None:
        """Sets the named property to the given value."""

        if type(value) != Point2D:
            raise Exception("Attempting to set non-Point2D in Point2D property: " + str(value))

        point_string = value.to_bracket_string()
        self._set_property(property_name, point_string, _PropertyUnits.User)

    def _get_point3D_property(self, property_name: str) -> Point3D:
        """Gets the value of the (Point3D) property with the given name."""

        point_string = self._get_property(property_name, _PropertyUnits.User)

        return Point3D.from_bracket_string(point_string)

    def _set_point3D_property(self, property_name: str, value: Point3D) -> None:
        """Sets the named property to the given value."""

        if type(value) != Point3D:
            raise Exception("Attempting to set non-Point3D in Point3D property: " + str(value))

        point_string = value.to_bracket_string()
        self._set_property(property_name, point_string, _PropertyUnits.User)


    # INTERNAL PROPERTY ACCESS OPERATIONS

    def _get_property(self, property_name: str, units: _PropertyUnits) -> str:
        """Gets the value (as a string) of the given property name, in the given units."""

        if (units == _PropertyUnits.Internal):
            command_name = "GET_PROP_INTERNAL"
        else:
            command_name = "GET_PROP_USER"

        cmd = "[" + command_name + "][" + property_name + "]"
        return self._command(cmd)

    def _set_property(self, property_name: str, value: str, units: _PropertyUnits) -> None:
        """Sets the given named property to the given value in the given units."""

        # we do this check at the lowest level (all setting goes through this method)
        _raise_if_invalid_string_property_value(value)

        if (units == _PropertyUnits.Internal):
            command_name = "SET_PROP_INTERNAL"
        else:
            command_name = "SET_PROP_USER"

        cmd = "[" + command_name + "][" + property_name + "][" + value + "]"
        self._command(cmd)
     
