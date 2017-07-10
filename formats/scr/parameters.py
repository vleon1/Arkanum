"""This module defines parameters required by script lines."""
import enum
from typing import Optional
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

    def __init__(self, type: Type, value: Optional[int]=None):
        """Initialize the object parameter.

        Arguments:
            type: The Object.Type of the object parameter.
            variable: Optional value attached to the parameter.
        """
        self.type = type
        self.value = value

    def __repr__(self):
        """Return a readable representation of the object.

        The format of the returned string is:
        "Object(type, value)"
        """
        return "Number({}, {})".format(self.type, self.value)


class Number(Parameter):
    """A script Number is a representation of an Integer.

    The game object will either directly store an int or will be used as a
    reference to some value store elsewhere.

    Attributes:
        type: The type of the number.
        value: Internal value or reference.
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

    def __init__(self, type: Type, value: int):
        """Initialize the Number object.

        The value argument is always an int, but will only be the actual
        "value" if type == Type.number. Otherwise the value acts as an id of
        the given type.

        Args:
            type: A Number.Type which determines the location of the int.
            variable: The value or reference given to the Number.
        """
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        """Return a readable representation of the number.

        Returns:
            String with format "Number(type, value)"
        """
        return "Number({}, {})".format(self.type, self.value)
