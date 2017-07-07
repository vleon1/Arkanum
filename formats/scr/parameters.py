import enum


class Object(enum.Enum):
    """A script Object is one or a collection of game objects that are attached
    to a specific script Action.
    """
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


class Number(object):
    """A script Number is a representation of an Integer.

    The object either directly stores are an int or is used as a reference to
    some value store elsewhere.

    Attributes:
        type: The type of the number.
        value: The current value attached to the type of the number.
    """

    # TODO: Implement all types.

    class Type(enum.Enum):
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
        the given type. Thus the value attribute does not always return the
        parameter with name "value" passed to this function.

        Args:
            type: A Number.Type which determines the location of the int.
            value: The value or reference given to the Number.
        """
        self.type = type
        self._value = value

    @property
    def value(self):
        if self.type == Number.Type.number:
            return self._value
        else:
            raise NotImplementedError

    @value.setter
    def value(self, new_value):
        if self.type == Number.Type.number:
            self._value = int(self.value)
        else:
            raise NotImplementedError

    def assign(self, new_value):
        self.value = new_value

    def __int__(self):
        return int(self.value)

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __sub__(self, other):
        return self.value - other

    def __rsub__(self, other):
        return other - self.value

    def __mul__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return other * self.value

    def __floordiv__(self, other):
        return self.value // other

    def __rfloordiv__(self, other):
        return other // self.value

    def __eq__(self, other):
        return self.value == other

    def __le__(self, other):
        return self.value <= other

    def __lt__(self, other):
        return self.value < other

    def __ge__(self, other):
        return self.value >= other

    def __gt__(self, other):
        return self.value > other

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return "Number({}, {})".format(self.type, self)
