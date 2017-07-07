from formats.scr import parameters
from formats.scr import actions


class Script(object):
    """The class describes a simple runnable script inside the game of Arcanum.

    A Script contains a header with basic information and a series of lines.
    Each line needs a callback to some game state variables, e.g. global flags
    or scenery in vicinity. Scripts are stored as files with the extension
    ".scr".

    Attributes:
        pc: The program counter or current line number of the script.
        lines: A list of lines that belong to the script.
        dialog: The dialog that is attached to the script.
        loop_objects: Objects to be looped over.
        loop_start: Line number where the current loop starts.\
        flags: Local flags of the script.
    """

    # .scr format is something like this:
    # 4 bytes- varflags
    # 4 bytes - counters
    # 38 bytes - description
    # 2 bytes - ?
    # 2 bytes - scriptflags
    # 2 bytes - ? probably unused scriptflags
    # 4 bytes - number of lines
    # 8 bytes - ?
    # num_lines * 132 bytes - Array of lines

    class Line(object):
        """A Line is single command called by a Script.

        A line is made up out of three parts.
        * A condition that is either true or false.
        * An action that will be executed if the condition is true.
        * An action that will be executed if the condition is false.

        Attributes:
            condition: A function that will be evaluated to decide which action
                to run.
            action: The function that will be called if the condition evaluates
                to true.
            params: A list of parameters that will be passed to action.
            else_action: The function that will be called if the condition
                evaluates to false.
            else_params: A list of parametsr that will be passed to
                else_action.
        """

        # serialized format is:
        # 4 bytes - condition code
        # 8 * 1 byte - param type
        # 8 * 4 bytes - param value
        # 4 bytes - if action code
        # 8 * 1 byte - param type
        # 8 * 4 bytes - param value
        # 4 bytes - then action code
        # 8 * 1 byte - param type
        # 8 * 4 bytes - param value

        def __init__(self,
                     condition=None,
                     action=None,
                     params=None,
                     else_action=None,
                     else_params=None):
            """Initializes a line object.

            All arguments are optional. A undefined condition will always
            evaluate to true, thus in that case the else action will never be
            called. Actions that are undefined simply do nothing.

            Args:
                condition: A callable object that is evaluated each time the
                    line is executed to decide which action to run.
                action: A callable function that will be called when the the
                    line is executed and condition evaluated to true.
                params: A list of parameters that will be passed to action.
                else_action: A callable function that will be called when the
                	line is executed and the condition is evaluated to false.
                else_params: A list of parameters that will be passed to
                    else_action.

            """
            self.action = action if action else actions.Action.do_nothing
            self.params = params if params else []
            self.condition = condition if condition else actions.Condition.true
            self.else_action = (else_action
                                if else_action else actions.Action.do_nothing)
            self.else_params = else_params if params else []

        def __call__(self, script):
            """Evaluate the condition and run the required action.

            Args:
                script: The script which runs this line.
            """
            if self.enabled:
                return self.action(*self.params, script=script)
            else:
                return self.else_action(*self.else_params, script=script)

        @property
        def enabled(self):
            return self.condition()

    def __init__(self):
        self.pc = 0
        self.lines = None
        self.dialog = None
        self.loop_objects = []
        self.loop_start = None
        self.flags = [False] * 4 * 8  # TODO: Create enum for this.

    def __call__(self, line=None):
        """Run the script starting at the current program counter or at
        specified line number.

        Args:
            line: Optional line number at which the script should start
                excecution.
        """
        if line:
            self.pc = line
        while True:
            res = self.lines[self.pc](self)
            if res == actions.ReturnCode.end:
                # TODO: Implement default return behaviour
                return
            elif res == actions.ReturnCode.end_skip:
                return
            elif res == actions.ReturnCode.goto_next:
                self.pc += 1
            else:
                self.pc = res.value
