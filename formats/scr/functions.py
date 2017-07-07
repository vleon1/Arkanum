import enum
import random


class ReturnCode(enum.IntEnum):
    """Objects used as return value by script actions.

    Every Action returns a member of this class. Every return code is an
    integer. All nonnegative integers are reserved for the "goto" member.
    """
    end = -2
    step = -1
    goto = 0

    @classmethod
    def _missing_(cls, value):
        if value > 0:
            pseudo_member = object.__new__(cls)
            pseudo_member._name_ = cls.goto._name_
            pseudo_member._value_ = value
            return pseudo_member
        else:
            super()._missing_(value)


def return_default():
    # TODO: default end behaviour
    return ReturnCode.end


def set_local_flag(flag, script=None):
    script.flags[flag] = True
    return ReturnCode.step


def clear_local_flag(flag, script=None):
    script.flags[flag] = False
    return ReturnCode.step


def num_assign(dst, src):
    dst.assign(src)
    return ReturnCode.step


def num_add(dst, src_1, src_2):
    dst.assign(src_1 + src_2)
    return ReturnCode.step


def num_sub(dst, src_1, src_2):
    dst.assign(src_1 - src_2)
    return ReturnCode.step


def num_mul(dst, src_1, src_2):
    dst.assign(src_1 * src_2)
    return ReturnCode.step


def num_div(dst, src_1, src_2):
    dst.assign(src_1 / src_2)
    return ReturnCode.step


def loop_start(objects, script=None):
    script.loop_objects = list(objects)
    script.loop_start = script.pc + 1
    return ReturnCode.step


def loop_end(objects, script=None):
    script.loop_objects.pop(0)
    return ReturnCode(script.loop_start)


def loop_break(script=None):
    # Find end of loop
    end = next(i for i, v in script.lines[script.pc:]
               if v.action == Action.loop_end)
    script.loop_objects = []
    script.loop_start = None
    return ReturnCode(script.pc + end + 1)


def random_number(min, max, dst):
    dst.assign(random.randint(min, max))
    return ReturnCode.step
