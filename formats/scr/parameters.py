"""This module defines parameters required by script lines."""
import enum
from typing import Optional, SupportsInt, Any
from formats.helpers import name


class Parameter(object):
    """Base class for parameter objects."""

    pass


class Object(Parameter):
    """An object parameter.

    A script Object is one or a collection of game objects that are attached
    to a specific script Action.
    """

    @name("Object.Type")
    class Type(enum.Enum):
        """The type of the object parameter."""

        triggerer = 0
        attachee = 1
        every_follower = 2
        any_follower = 3
        everyone_in_party = 4
        anyone_in_party = 5
        everyone_in_team = 6
        anyone_in_team = 7
        everyone_in_vicinity = 8
        anyone_in_vicinity = 9
        current_looped_object = 10
        local_object = 11
        extra_object = 12
        everyone_in_group = 13
        anyone_in_group = 14
        every_scenery_in_vicinity = 15
        any_scenery_in_vicinity = 16
        every_container_in_vicinity = 17
        any_container_in_vicinity = 18
        every_portal_in_vicinity = 19
        any_portal_in_vicinity = 20
        player = 21
        every_item_in_vicinity = 22
        any_item_in_vicinity = 23

    def __init__(self, type: Type, variable: Optional[int]=None):
        """Initialize the object parameter.

        Arguments:
            type: The Object.Type of the object parameter.
            variable: Optional value attached to the parameter.
        """
        self.type = type
        self.variable = variable


class Number(Parameter):
    """A script Number is a representation of an Integer.

    The object either directly stores are an int or is used as a reference to
    some value store elsewhere.

    Attributes:
        type: The type of the number.
        variable: Internal value or reference.
        value: The current value attached to the type of the number.
    """

    @name("Number.Type")
    class Type(enum.Enum):
        """The type of the number parameter."""

        counter = 0
        global_var = 1
        local_var = 2
        number = 3
        global_flag = 4
        pc_var = 5
        pc_flag = 6

    def __init__(self, type: Type, variable: int):
        """Initialize the Number object.

        The variable argument is always an int, but will only be the actual
        "value" if type == Type.number. Otherwise the variable acts as an id of
        the given type.

        Args:
            type: A Number.Type which determines the location of the int.
            variable: The value or reference given to the Number.
        """
        self.type = type
        self.variable = variable

    @property
    def value(self):
        """The relative value of the number.

        This will always refer to value deferred by the type and the internal
        value. Thus if the the type is a global variable and the internal value
        is 0 the value of global variable 0 will be the target.
        """
        if self.type == Number.Type.number:
            return self.variable
        else:
            raise NotImplementedError

    @value.setter
    def value(self, new_value: SupportsInt):
        if self.type == Number.Type.number:
            self.variable = int(new_value)
        else:
            raise NotImplementedError

    def assign(self, new_value: SupportsInt):
        """Assign a new value to the number."""
        self.value = new_value

    def __int__(self):
        """Return the number as an int."""
        return int(self.value)

    def __add__(self, other: Any):
        """Same as 'self.value + other'."""
        return self.value + other

    def __radd__(self, other: Any):
        """Same as 'other + self.value'."""
        return other + self.value

    def __sub__(self, other: Any):
        """Same as 'self.value - other'."""
        return self.value - other

    def __rsub__(self, other: Any):
        """Same as 'other - self.value'."""
        return other - self.value

    def __mul__(self, other: Any):
        """Same as 'self.value * other'."""
        return self.value * other

    def __rmul__(self, other: Any):
        """Same as 'other * self.value'."""
        return other * self.value

    def __floordiv__(self, other: Any):
        """Same as 'self.value // other'."""
        return self.value // other

    def __rfloordiv__(self, other: Any):
        """Same as 'other // self.value'."""
        return other // self.value

    def __eq__(self, other: Any):
        """Same as 'self.value == other'."""
        return self.value == other

    def __le__(self, other: Any):
        """Same as 'self.value <= other'."""
        return self.value <= other

    def __lt__(self, other: Any):
        """Same as 'self.value < other'."""
        return self.value < other

    def __ge__(self, other: Any):
        """Same as 'self.value >= other'."""
        return self.value >= other

    def __gt__(self, other: Any):
        """Same as 'self.value > other'."""
        return self.value > other

    def __str__(self):
        """Return the value of the number as string."""
        return str(self.value)

    def __repr__(self):
        """Return a representation of the actual object.

        The format of the returned string is:
        "Number(type, internal_value)"
        """
        return "Number({}, {})".format(self.type, self.variable)
