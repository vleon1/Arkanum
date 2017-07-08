"""This modules defines the format and parsing of a line in a script file."""
from formats.helpers import IntEnumPlus, FileStruct
from formats.scr.parameters import Number, Object

_N = (Number,)
_NN = (Number, Number)
_NNN = (Number, Number, Number)
_NNNN = (Number, Number, Number, Number)
_NNNONN = (Number, Number, Number, Object, Number, Number)
_NNOO = (Number, Number, Object, Object)
_NNOON = (Number, Number, Object, Object, Number)
_NO = (Number, Object)
_NON = (Number, Object, Number)
_NOON = (Number, Object, Object, Number)
_NOOON = (Number, Object, Object, Object, Number)
_O = (Object,)
_ON = (Object, Number)
_ONN = (Object, Number, Number)
_ONNN = (Object, Number, Number, Number)
_ONNO = (Object, Number, Number, Object)
_ONO = (Object, Number, Object)
_OO = (Object, Object)
_OON = (Object, Object, Number)
_OOONN = (Object, Object, Object, Number, Number)


class Action(IntEnumPlus):
    """The enum defines the actions of scripts with the parameters they take.

    Desriptions can be found in "semes/action.mes"
    """

    do_nothing = 0
    return_skip = 1
    return_default = 2
    goto_line = 3, _N
    dialog = 4, _N
    remove_this_script = 5
    replace_this_script = 6, _N
    call_script = 7, _NNOO
    set_local_flag = 8, _N
    clear_local_flag = 9, _N
    num_assign = 10, _NN
    num_add = 11, _NNN
    num_sub = 12, _NNN
    num_mul = 13, _NNN
    num_div = 14, _NNN
    obj_assign = 15, _OO
    set_pc_quest_state = 16, _ONN
    set_global_quest_state = 17, _NN
    loop_start = 18, _O
    loop_end = 19
    loop_break = 20
    follow = 21, _OO
    unfollow = 22, _O
    float_line = 23, _NO
    print_line = 24, _NN
    add_blessing = 25, _NO
    remove_blessing = 26, _NO
    add_curse = 27, _NO
    remove_curse = 28, _NO
    get_reaction = 29, _OON
    set_reaction = 30, _OON
    adjust_reation = 31, _OON
    get_armor = 32, _ON
    get_stat = 33, _NON
    get_type = 34, _ON
    adjust_gold = 35, _ON
    attack = 36, _OO
    random_nber = 37, _NNN
    get_social_class = 38, _ON
    get_origin = 39, _ON
    transform_attachee = 40, _N
    transfer_item = 41, _NO
    get_story_state = 42, _N
    set_story_state = 43, _N
    teleport = 44, _ONNN
    set_day_standpoint = 45, _ONN
    set_night_standpoint = 46, _ONN
    get_skill = 47, _NON
    cast_spell_from = 48, _ONO
    mark_map = 49, _NO
    set_rumor = 50, _NO
    quell_rumor = 51, _NO
    create_object = 52, _NO
    set_lock_state = 53, _ON
    call_script_delayed = 54, _NNOON
    call_script_at_second = 55, _NNOON
    toggle_state = 56, _O
    toggle_invulnerability = 57, _O
    kill = 58, _O
    set_art = 59, _ON
    damage = 60, _ONN
    cast_spell = 61, _NO
    play_animation = 62, _ON
    give_xp = 63, _ON
    open_book = 64, _NO
    open_image = 65, _NO
    give_item = 66, _NO
    wait = 67, _O
    destroy = 68, _O
    walk = 69, _ONN
    get_weapon = 70, _ON
    get_distance = 71, _OON
    set_reputation = 72, _ON
    remove_reputation = 73, _ON
    run = 74, _OON
    heal = 75, _ON
    heal_fatigue = 76, _ON
    give_effect = 77, _ONN
    remove_effect = 78, _ON
    use_object = 79, _OOONN
    get_aptitude_on = 80, _NOOON
    call_attached_script = 81, _ONNO
    play_sound = 82, _N
    play_sound_at = 83, _NO
    get_area = 84, _ON
    queue_newspaper = 85, _N
    float_newspaper = 86, _O
    play_sound_scheme = 87, _N
    toggle_open_closed = 88, _O
    get_faction = 89, _ON
    get_scroll_distance = 90, _N
    get_aptitude = 91, _NOON
    rename = 92, _ON
    make_prone = 93, _O
    set_written_start = 94, _ON
    get_location = 95, _ONN
    get_days_since_start = 96, _N
    get_hour = 97, _N
    get_minute = 98, _N
    change_attached_script = 99, _ONN
    set_global_flag = 100, _N
    clear_global_flag = 101, _N
    fade_teleport = 102, _NNNONN
    fade = 103, _NNNN
    play_spell_eye_candy = 104, _NO
    get_hours_since_start = 105, _N
    toggle_sector_block = 106, _NN
    get_hp = 107, _ONN
    get_fatigue = 108, _ONN
    stop_attack = 109, _O
    toggle_monstergen = 110, _N
    get_armor_coverage = 111, _ON
    give_spell_mastery = 112, _ON
    unfog_townmap = 113, _N
    open_plaque = 114, _NO
    steal_100_gold = 115, _OO
    stop_spell_eye_candy = 116, _NO
    give_fate_point = 117, _O
    cast_spell_from_free = 118, _ONO
    set_pc_quest_state_to_unbotched = 119, _ON
    play_script_eye_candy = 120, _NO
    cast_spell_from_irresistible = 121, _ONO
    cast_spell_from_free_irresistible = 122, _ONO
    touch_art = 123, _N
    stop_script_eye_candy = 124, _NO
    remove_script_from_queue = 125, _NO
    destroy_item = 126, _NO
    toggle_inventory_display = 127, _O
    heal_poison = 128, _ON
    open_schematic = 129, _O
    stop_spell = 130, _NO
    queue_slide = 131, _N
    end_game = 132
    set_rotation = 133, _ON
    set_faction = 134, _ON
    drain_charges = 135, _NO
    cast_spell_irresistible = 136, _NO
    adjust_stat = 137, _NON
    damage_irresistible = 138
    set_autolevel_scheme = 139, _ON
    set_day_standpoint_on_map = 140, _ONN
    set_night_standpoint_on_map = 141, _ONN

    def __init__(self, value, parameters=()):
        """Initialize the action.

        Arguments:
            value: The integer representation of the action.
            parameters: The parameters used by the action.
        """
        self.params = parameters


class Condition(IntEnumPlus):
    """Defines a condition on a script line.

    Conditions are used to decide the action to execute on a given
    line. Desriptions can be found in "semes/condition.mes"
    """

    true = 0
    is_daytime = 1
    has_gold = 2, _ON
    local_flag = 3, _N
    num_eq = 4, _NN
    num_le = 5, _NN
    pc_quest_has_state = 6, _ON
    global_quest_has_state = 7, _NN
    has_blessing = 8, _ON
    has_curse = 9, _ON
    has_met_npc = 10, _OO
    has_bad_associates = 11, _O
    is_polymorphed = 12, _O
    is_shrunk = 13, _O
    has_a_body_spell = 14, _O
    is_invisible = 15, _O
    has_mirror_image = 16, _O
    has_item = 17, _ON
    is_follower = 18, _OO
    is_species = 19, _ON
    is_named = 20, _ON
    is_wielding_item = 21, _ON
    is_dead = 22, _O
    has_maximum_followers = 23, _O
    can_open_container = 24, _OO
    has_surrendered = 25, _O
    is_in_dialog = 26, _O
    is_switched_off = 27, _O
    can_see_object = 28, _OO
    can_hear_object = 29, _OO
    is_invulnerable = 30, _O
    is_in_combat = 31, _O
    is_at_location = 32, _ONN
    has_reputation = 33, _ON
    is_within_n_tiles_of_location = 34, _ONNN
    is_under_the_influence_of_spell = 35, _ON
    is_open = 36, _O
    is_an_animal = 37, _O
    is_undead = 38, _O
    was_jilted_by_a_pc = 39, _O
    pc_knows_rumor = 40, _ON
    rumor_has_been_quelled = 41, _N
    is_busted = 42, _O
    global_flag = 43, _N
    can_open_portal = 44, _OON
    sector_is_blocked = 45, _NN
    monster_generator_is_disabled = 46, _N
    is_identified = 47, _O
    knows_spell = 48, _ON
    has_mastered_spell_college = 49, _ON
    items_are_being_rewielded = 50
    is_prowling = 51, _O
    is_waiting = 52, _O

    def __init__(self, value, parameters=()):
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

    Each part can take aditional parameters which a defined by the type of the
    that part.

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
                 condition=None,
                 condition_params=(),
                 action=None,
                 action_params=(),
                 else_action=None,
                 else_action_params=()):
        """Initialize a line object.

        All arguments are optional. A undefined condition will always
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
            values = [p.variable for p in params]
            return (*types, *remainder, *values, *remainder)

        raw_data = (self.condition.value, *pack_params(self.condition_params),
                    self.action.value, *pack_params(self.action_params),
                    self.else_action.value,
                    *pack_params(self.else_action_params))

        self.parser.pack_into_file(script_file, *raw_data)
