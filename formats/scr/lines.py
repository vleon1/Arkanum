"""This modules defines the format and parsing of a line in a script file."""
import enum
from formats.helpers import IntEnumPlus, FileStruct
from formats.scr.parameters import Number, Object, Parameter
from typing import Any, Iterable, Optional

_PARAMS_N = (Number,)
_PARAMS_NN = (Number, Number)
_PARAMS_NNN = (Number, Number, Number)
_PARAMS_NNNN = (Number, Number, Number, Number)
_PARAMS_NNNONN = (Number, Number, Number, Object, Number, Number)
_PARAMS_NNOO = (Number, Number, Object, Object)
_PARAMS_NNOON = (Number, Number, Object, Object, Number)
_PARAMS_NO = (Number, Object)
_PARAMS_NON = (Number, Object, Number)
_PARAMS_NOON = (Number, Object, Object, Number)
_PARAMS_NOOON = (Number, Object, Object, Object, Number)
_PARAMS_O = (Object,)
_PARAMS_ON = (Object, Number)
_PARAMS_ONN = (Object, Number, Number)
_PARAMS_ONNN = (Object, Number, Number, Number)
_PARAMS_ONNO = (Object, Number, Number, Object)
_PARAMS_ONO = (Object, Number, Object)
_PARAMS_OO = (Object, Object)
_PARAMS_OON = (Object, Object, Number)
_PARAMS_OOONN = (Object, Object, Object, Number, Number)


@enum.unique
class Action(IntEnumPlus):
    """The enum defines the actions of scripts with the parameters they take.

    Desriptions can be found in "semes/action.mes"
    """

    do_nothing = 0
    return_skip = 1
    return_default = 2
    goto_line = 3, _PARAMS_N
    dialog = 4, _PARAMS_N
    remove_this_script = 5
    replace_this_script = 6, _PARAMS_N
    call_script = 7, _PARAMS_NNOO
    set_local_flag = 8, _PARAMS_N
    clear_local_flag = 9, _PARAMS_N
    num_assign = 10, _PARAMS_NN
    num_add = 11, _PARAMS_NNN
    num_sub = 12, _PARAMS_NNN
    num_mul = 13, _PARAMS_NNN
    num_div = 14, _PARAMS_NNN
    obj_assign = 15, _PARAMS_OO
    set_pc_quest_state = 16, _PARAMS_ONN
    set_global_quest_state = 17, _PARAMS_NN
    loop_start = 18, _PARAMS_O
    loop_end = 19
    loop_break = 20
    follow = 21, _PARAMS_OO
    unfollow = 22, _PARAMS_O
    float_line = 23, _PARAMS_NO
    print_line = 24, _PARAMS_NN
    add_blessing = 25, _PARAMS_NO
    remove_blessing = 26, _PARAMS_NO
    add_curse = 27, _PARAMS_NO
    remove_curse = 28, _PARAMS_NO
    get_reaction = 29, _PARAMS_OON
    set_reaction = 30, _PARAMS_OON
    adjust_reation = 31, _PARAMS_OON
    get_armor = 32, _PARAMS_ON
    get_stat = 33, _PARAMS_NON
    get_type = 34, _PARAMS_ON
    adjust_gold = 35, _PARAMS_ON
    attack = 36, _PARAMS_OO
    random_nber = 37, _PARAMS_NNN
    get_social_class = 38, _PARAMS_ON
    get_origin = 39, _PARAMS_ON
    transform_attachee = 40, _PARAMS_N
    transfer_item = 41, _PARAMS_NO
    get_story_state = 42, _PARAMS_N
    set_story_state = 43, _PARAMS_N
    teleport = 44, _PARAMS_ONNN
    set_day_standpoint = 45, _PARAMS_ONN
    set_night_standpoint = 46, _PARAMS_ONN
    get_skill = 47, _PARAMS_NON
    cast_spell_from = 48, _PARAMS_ONO
    mark_map = 49, _PARAMS_NO
    set_rumor = 50, _PARAMS_NO
    quell_rumor = 51, _PARAMS_NO
    create_object = 52, _PARAMS_NO
    set_lock_state = 53, _PARAMS_ON
    call_script_delayed = 54, _PARAMS_NNOON
    call_script_at_second = 55, _PARAMS_NNOON
    toggle_state = 56, _PARAMS_O
    toggle_invulnerability = 57, _PARAMS_O
    kill = 58, _PARAMS_O
    set_art = 59, _PARAMS_ON
    damage = 60, _PARAMS_ONN
    cast_spell = 61, _PARAMS_NO
    play_animation = 62, _PARAMS_ON
    give_xp = 63, _PARAMS_ON
    open_book = 64, _PARAMS_NO
    open_image = 65, _PARAMS_NO
    give_item = 66, _PARAMS_NO
    wait = 67, _PARAMS_O
    destroy = 68, _PARAMS_O
    walk = 69, _PARAMS_ONN
    get_weapon = 70, _PARAMS_ON
    get_distance = 71, _PARAMS_OON
    set_reputation = 72, _PARAMS_ON
    remove_reputation = 73, _PARAMS_ON
    run = 74, _PARAMS_OON
    heal = 75, _PARAMS_ON
    heal_fatigue = 76, _PARAMS_ON
    give_effect = 77, _PARAMS_ONN
    remove_effect = 78, _PARAMS_ON
    use_object = 79, _PARAMS_OOONN
    get_aptitude_on = 80, _PARAMS_NOOON
    call_attached_script = 81, _PARAMS_ONNO
    play_sound = 82, _PARAMS_N
    play_sound_at = 83, _PARAMS_NO
    get_area = 84, _PARAMS_ON
    queue_newspaper = 85, _PARAMS_N
    float_newspaper = 86, _PARAMS_O
    play_sound_scheme = 87, _PARAMS_N
    toggle_open_closed = 88, _PARAMS_O
    get_faction = 89, _PARAMS_ON
    get_scroll_distance = 90, _PARAMS_N
    get_aptitude = 91, _PARAMS_NOON
    rename = 92, _PARAMS_ON
    make_prone = 93, _PARAMS_O
    set_written_start = 94, _PARAMS_ON
    get_location = 95, _PARAMS_ONN
    get_days_since_start = 96, _PARAMS_N
    get_hour = 97, _PARAMS_N
    get_minute = 98, _PARAMS_N
    change_attached_script = 99, _PARAMS_ONN
    set_global_flag = 100, _PARAMS_N
    clear_global_flag = 101, _PARAMS_N
    fade_teleport = 102, _PARAMS_NNNONN
    fade = 103, _PARAMS_NNNN
    play_spell_eye_candy = 104, _PARAMS_NO
    get_hours_since_start = 105, _PARAMS_N
    toggle_sector_block = 106, _PARAMS_NN
    get_hp = 107, _PARAMS_ONN
    get_fatigue = 108, _PARAMS_ONN
    stop_attack = 109, _PARAMS_O
    toggle_monstergen = 110, _PARAMS_N
    get_armor_coverage = 111, _PARAMS_ON
    give_spell_mastery = 112, _PARAMS_ON
    unfog_townmap = 113, _PARAMS_N
    open_plaque = 114, _PARAMS_NO
    steal_100_gold = 115, _PARAMS_OO
    stop_spell_eye_candy = 116, _PARAMS_NO
    give_fate_point = 117, _PARAMS_O
    cast_spell_from_free = 118, _PARAMS_ONO
    set_pc_quest_state_to_unbotched = 119, _PARAMS_ON
    play_script_eye_candy = 120, _PARAMS_NO
    cast_spell_from_irresistible = 121, _PARAMS_ONO
    cast_spell_from_free_irresistible = 122, _PARAMS_ONO
    touch_art = 123, _PARAMS_N
    stop_script_eye_candy = 124, _PARAMS_NO
    remove_script_from_queue = 125, _PARAMS_NO
    destroy_item = 126, _PARAMS_NO
    toggle_inventory_display = 127, _PARAMS_O
    heal_poison = 128, _PARAMS_ON
    open_schematic = 129, _PARAMS_O
    stop_spell = 130, _PARAMS_NO
    queue_slide = 131, _PARAMS_N
    end_game = 132
    set_rotation = 133, _PARAMS_ON
    set_faction = 134, _PARAMS_ON
    drain_charges = 135, _PARAMS_NO
    cast_spell_irresistible = 136, _PARAMS_NO
    adjust_stat = 137, _PARAMS_NON
    damage_irresistible = 138
    set_autolevel_scheme = 139, _PARAMS_ON
    set_day_standpoint_on_map = 140, _PARAMS_ONN
    set_night_standpoint_on_map = 141, _PARAMS_ONN

    def __init__(self, value: int, parameters: Any=()):
        """Initialize the action.

        Arguments:
            value: The integer representation of the action.
            parameters: The parameters used by the action.
        """
        self.params = parameters


@enum.unique
class Condition(IntEnumPlus):
    """Defines a condition on a script line.

    Conditions are used to decide the action to execute on a given
    line. Desriptions can be found in "semes/condition.mes"
    """

    true = 0
    is_daytime = 1
    has_gold = 2, _PARAMS_ON
    local_flag = 3, _PARAMS_N
    num_eq = 4, _PARAMS_NN
    num_le = 5, _PARAMS_NN
    pc_quest_has_state = 6, _PARAMS_ON
    global_quest_has_state = 7, _PARAMS_NN
    has_blessing = 8, _PARAMS_ON
    has_curse = 9, _PARAMS_ON
    has_met_npc = 10, _PARAMS_OO
    has_bad_associates = 11, _PARAMS_O
    is_polymorphed = 12, _PARAMS_O
    is_shrunk = 13, _PARAMS_O
    has_a_body_spell = 14, _PARAMS_O
    is_invisible = 15, _PARAMS_O
    has_mirror_image = 16, _PARAMS_O
    has_item = 17, _PARAMS_ON
    is_follower = 18, _PARAMS_OO
    is_species = 19, _PARAMS_ON
    is_named = 20, _PARAMS_ON
    is_wielding_item = 21, _PARAMS_ON
    is_dead = 22, _PARAMS_O
    has_maximum_followers = 23, _PARAMS_O
    can_open_container = 24, _PARAMS_OO
    has_surrendered = 25, _PARAMS_O
    is_in_dialog = 26, _PARAMS_O
    is_switched_off = 27, _PARAMS_O
    can_see_object = 28, _PARAMS_OO
    can_hear_object = 29, _PARAMS_OO
    is_invulnerable = 30, _PARAMS_O
    is_in_combat = 31, _PARAMS_O
    is_at_location = 32, _PARAMS_ONN
    has_reputation = 33, _PARAMS_ON
    is_within_n_tiles_of_location = 34, _PARAMS_ONNN
    is_under_the_influence_of_spell = 35, _PARAMS_ON
    is_open = 36, _PARAMS_O
    is_an_animal = 37, _PARAMS_O
    is_undead = 38, _PARAMS_O
    was_jilted_by_a_pc = 39, _PARAMS_O
    pc_knows_rumor = 40, _PARAMS_ON
    rumor_has_been_quelled = 41, _PARAMS_N
    is_busted = 42, _PARAMS_O
    global_flag = 43, _PARAMS_N
    can_open_portal = 44, _PARAMS_OON
    sector_is_blocked = 45, _PARAMS_NN
    monster_generator_is_disabled = 46, _PARAMS_N
    is_identified = 47, _PARAMS_O
    knows_spell = 48, _PARAMS_ON
    has_mastered_spell_college = 49, _PARAMS_ON
    items_are_being_rewielded = 50
    is_prowling = 51, _PARAMS_O
    is_waiting = 52, _PARAMS_O

    def __init__(self, value: int, parameters: Any=()):
        """Initialize the condition.

        Arguments:
            value: The integer representation of the condition.
            parameters: The parameters used by the condition.
        """
        self.params = parameters


class Line(object):
    """A Line is single command called by a Script.

    A line is made up out of three parts.
    * A condition that is either true or false.
    * An action that will be executed if the condition is true.
    * An action that will be executed if the condition is false.

    Each part can take aditional parameters which are defined by the type of
    the that part.

    Attributes:
        condition: A condition.
        condition_params: The specified parameters of the condition.
        action: The action called when the condition is true.
        action_params: The specified parameters of true_action.
        else_action: The action called when the condition is false.
        else_action_params: The specified parameters of else_action.
    """

    condition_code_format = "I"
    param_type_format = "B"
    param_value_format = "I"
    action_code_format = "I"

    params_format = "8{}8{}".format(param_type_format, param_value_format)
    condition_format = "{}{}".format(condition_code_format, params_format)
    action_format = "{}{}".format(action_code_format, params_format)
    full_format = "{}{}{}".format(condition_format, action_format,
                                  action_format)

    parser = FileStruct(full_format)

    def __init__(self,
                 condition: Optional[Condition]=None,
                 condition_params: Iterable[Parameter]=(),
                 action: Optional[Action]=None,
                 action_params: Iterable[Parameter]=(),
                 else_action: Optional[Action]=None,
                 else_action_params: Iterable[Parameter]=()):
        """Initialize a line object.

        All arguments are optional. An undefined condition will always
        evaluate to true, thus in that case the else action will never be
        called. Actions that are undefined simply do nothing.

        Args:
            condition: A condition.
            condition_params: The specified parameters of the condition.
            action: The action called when the condition is true.
            action_params: The specified parameters of true_action.
            else_action: The action called when the condition is false.
            else_action_params: The specified parameters of else_action.
        """
        self.condition = condition if condition else Condition.true
        self.condition_params = condition_params
        self.action = action if action else Action.do_nothing
        self.action_params = action_params
        self.else_action = else_action if else_action else Action.do_nothing
        self.else_action_params = else_action_params

    @classmethod
    def read_from(cls, script_file: str) -> "Line":
        """Deserialize a script line from the given file.

        Arguments:
            script_file: An open script file.

        Returns:
            New Script Line object.
        """
        raw_data = cls.parser.unpack_from_file(script_file)

        def parse_param(cls, type, val):
            return cls(cls.Type(type), val)

        condition = Condition(raw_data[0])
        condition_params = tuple(
            map(parse_param, condition.params, raw_data[1:9], raw_data[9:17]))
        action = Action(raw_data[17])
        action_params = tuple(
            map(parse_param, action.params, raw_data[18:26], raw_data[26:34]))
        else_action = Action(raw_data[34])
        else_action_params = tuple(
            map(parse_param, else_action.params, raw_data[35:43], raw_data[
                43:51]))

        return cls(
            condition=condition,
            condition_params=condition_params,
            action=action,
            action_params=action_params,
            else_action=else_action,
            else_action_params=else_action_params)

    def write_to(self, script_file: str) -> None:
        """Serialize a script line in the given file.

        Arguments:
            script_file: An open script file.
        """
        def pack_params(params):
            remainder = [0] * (8 - len(params))
            types = [p.type.value for p in params]
            values = [p.value for p in params]
            return (*types, *remainder, *values, *remainder)

        raw_data = (self.condition.value, *pack_params(self.condition_params),
                    self.action.value, *pack_params(self.action_params),
                    self.else_action.value,
                    *pack_params(self.else_action_params))

        self.parser.pack_into_file(script_file, *raw_data)

    def __str__(self) -> str:
        """Return line in readable format.

        Returns:
            The line as a readable string.
        """
        action_str = "{}{}".format(self.action.name, self.action_params)
        condition_str = " if {}{}".format(
            self.condition.name,
            self.condition_params) if self.condition != Condition.true else ""
        else_str = " else {}{}".format(
            self.else_action.name, self.else_action_params
        ) if self.else_action != Action.do_nothing else ""

        return "{}{}{}".format(action_str, condition_str, else_str)
