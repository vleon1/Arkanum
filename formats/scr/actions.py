import enum
from formats.scr import functions as f


def todo():
    raise NotImplementedError()


class FunctionEnum(enum.Enum):
    """Implementation of an enum class where each member is a callable
    function.
    """

    def __new__(cls, value, func):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, value, func):
        self._value_ = value
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, *kwargs)


class Action(FunctionEnum):
    """Enum class of actions that can be run inside a script.

    Each action will return a ReturnCode a specified in the
    formats.scr.functions module.
    """
    do_nothing = 0, lambda: f.ReturnCode.step
    return_skip = 1, lambda: f.ReturnCode.end
    return_default = 2, f.return_default
    goto_line = 3, lambda line: f.ReturnCode(line)
    dialog = 4, lambda dialog_line: todo()
    remove_this_script = 5, lambda: todo()
    replace_this_script = 6, lambda script_id: todo()
    call_script = 7, lambda script_id, line, triggerer, attachee: todo()
    set_local_flag = 8, f.set_local_flag
    clear_local_flag = 9, f.clear_local_flag
    num_assign = 10, f.num_assign
    num_add = 11, f.num_add
    num_sub = 12, f.num_sub
    num_mul = 13, f.num_mul
    num_div = 14, f.num_div
    obj_assign = 15, lambda dst, src: todo()
    set_pc_quest_state = 16, lambda pc, quest_id, state: todo()
    set_global_quest_state = 17, lambda quest_id, state: todo()
    loop_start = 18, f.loop_start
    loop_end = 19, f.loop_end
    loop_break = 20, f.loop_break
    critter_follow = 21, lambda critter, target: todo()
    critter_unfollow = 22, lambda critter: todo()
    float_line = 23, lambda line, obj: todo()
    print_line = 24, lambda line, message_class: todo()
    add_blessing = 25, lambda blessing_id, target: todo()
    remove_blessing = 26, lambda blessing_id, target: todo()
    add_curse = 27, lambda curse_id, target: todo()
    remove_curse = 28, lambda curse_id, target: todo()
    get_reaction = 29, lambda npc, pc, dst: todo()
    set_reaction = 30, lambda npc, pc, src: todo()
    adjust_reation = 31, lambda npc, pc, value: todo()
    get_armor = 32, lambda target, dst: todo()
    get_stat = 33, lambda stat_id, target, dst: todo()
    get_object_type = 34, lambda target, dst: todo()
    adjust_gold = 35, lambda target, value: todo()
    attack = 36, lambda src, dst: todo()
    random_number = 37, f.random_number
    get_social_class = 38, lambda target, dst: todo()
    # TODO: all below
    # origin of npc (obj): store in (num) = 39, lambda: todo()
    # transform Attachee into basic prototype (num) = 40, lambda: todo()
    # transfer item named (num) from (obj) to (obj) = 41, lambda: todo()
    # story state: store in (num) = 42, lambda: todo()
    # story state: set to (num) = 43, lambda: todo()
    # teleport (obj) to map (num) at X:(num) Y:(num) = 44, lambda: todo()
    # set day standpoint of critter (obj) to X:(num) Y:(num) on this map = 45, lambda: todo()
    # set night standpoint of critter (obj) to X:(num) Y:(num) on this map = 46, lambda: todo()
    # skill (num) of (obj): store in (num) = 47, lambda: todo()
    # spells: have (obj) cast spell (num) on (obj) = 48, lambda: todo()
    # mark map location (num) of pc (obj) as known = 49, lambda: todo()
    # rumor: set rumor (num) for pc (obj) = 50, lambda: todo()
    # rumor: quell rumor (num) for pc (obj) = 51, lambda: todo()
    # create object with basic prototype (num) near (obj) = 52, lambda: todo()
    # lock state of (obj): set to (num) = 53, lambda: todo()
    # call script (num) at line (num) with triggerer (obj) and attachee (obj) in (num) seconds = 54, lambda: todo()
    # call script (num) at line (num) with triggerer (obj) and attachee (obj) at second (num) = 55, lambda: todo()
    # toggle (obj) state on/off = 56, lambda: todo()
    # toggle (obj) invulnerability = 57, lambda: todo()
    # kill (obj) = 58, lambda: todo()
    # change art num of (obj) to (num) = 59, lambda: todo()
    # damage (obj) for (num) points of type (num) damage = 60, lambda: todo()
    # spells: cast spell (num) on (obj) = 61, lambda: todo()
    # have (obj) perform animation (num) = 62, lambda: todo()
    # give (obj) xps for a quest level (num) = 63, lambda: todo()
    # written UI start: book (num) for reader (obj) = 64, lambda: todo()
    # written UI start: image (num) for reader (obj) = 65, lambda: todo()
    # create item with basic prototype (num) inside (obj) = 66, lambda: todo()
    # have critter (obj) wait for his leader = 67, lambda: todo()
    # destroy (obj) = 68, lambda: todo()
    # have critter (obj) walk to X:(num) Y:(num) = 69, lambda: todo()
    # weapon of (obj): get in (num) = 70, lambda: todo()
    # distance between (obj) and (obj): get in (num) = 71, lambda: todo()
    # reputation: give (obj) the reputation (num) = 72, lambda: todo()
    # reputation: remove from (obj) the reputation (num) = 73, lambda: todo()
    # have critter (obj) run to X:(num) Y:(num) = 74, lambda: todo()
    # heal (obj) for (num) points = 75, lambda: todo()
    # heal (obj) for (num) fatigue points = 76, lambda: todo()
    # give (obj) the effect (num) with cause (num) = 77, lambda: todo()
    # remove from (obj) the effect (num) = 78, lambda: todo()
    # have (obj) use (obj) on (obj) using skill (num) with modifier (num) = 79, lambda: todo()
    # magic/tech: adjust (num) by item (obj) used by (obj) on (obj): store in (num) = 80, lambda: todo()
    # call script attached to (obj) at point (num) at line (num) with triggerer (obj) = 81, lambda: todo()
    # play sound (num) = 82, lambda: todo()
    # play sound (num) at (obj) = 83, lambda: todo()
    # area of (obj): store in (num) = 84, lambda: todo()
    # newspaper: queue (num) with priority (num) = 85, lambda: todo()
    # newspaper: float current headline over (obj) = 86, lambda: todo()
    # play sound scheme (num) and (num) = 87, lambda: todo()
    # toggle (obj) open/closed = 88, lambda: todo()
    # faction of npc (obj): store in (num) = 89, lambda: todo()
    # scroll distance: store in (num) = 90, lambda: todo()
    # magic/tech: adjust (num) by item (obj) used by (obj): store in (num) = 91, lambda: todo()
    # rename (obj) as (num) = 92, lambda: todo()
    # have (obj) instantly become prone = 93, lambda: todo()
    # written start in (obj) set to (num) = 94, lambda: todo()
    # get location of (obj) and store X in (num) and Y in (num) = 95, lambda: todo()
    # day: store days since startup in (num) = 96, lambda: todo()
    # hour: store current game hour in (num) = 97, lambda: todo()
    # minute: store current game minute in (num) = 98, lambda: todo()
    # change script attached to (obj) at point (num) to script (num) = 99, lambda: todo()
    # set global flag (num) to true = 100, lambda: todo()
    # clear global flag (num) = 101, lambda: todo()
    # fade and teleport: pass (num) seconds, play (num) sound, play (num) movie, and teleport (obj) to map (num) at X:(num) Y:(num) = 102, lambda: todo()
    # fade: pass (num) seconds, play (num) sound, and play (num) movie, with (num) seconds during fade = 103, lambda: todo()
    # spell eye candy: play (num) on (obj) = 104, lambda: todo()
    # hour: store hours since startup in (num) = 105, lambda: todo()
    # toggle the blocked state of sector at location X:(num) and Y:(num) = 106, lambda: todo()
    # hit points of (obj): store current in (num) and maximum in (num) = 107, lambda: todo()
    # fatigue of critter (obj): store current in (num) and maximum in (num) = 108, lambda: todo()
    # combat: force (obj) to stop attacking = 109, lambda: todo()
    # toggle monster generator (num) on/off = 110, lambda: todo()
    # armor coverage of item (obj): store in (num) = 111, lambda: todo()
    # give (obj) spell mastery in college (num) = 112, lambda: todo()
    # unfog townmap (num) = 113, lambda: todo()
    # written UI start: plaque (num) for reader (obj) = 114, lambda: todo()
    # have (obj) try to steal 100 coins from (obj) = 115, lambda: todo()
    # spell eye candy: stop (num) on (obj) = 116, lambda: todo()
    # grant one fate point to (obj) = 117, lambda: todo()
    # spells: have (obj) cast free spell (num) on (obj) = 118, lambda: todo()
    # set PC (obj) quest (num) to state unbotched = 119, lambda: todo()
    # script eye candy: play (num) on (obj) = 120, lambda: todo()
    # spells: have (obj) cast unresistable spell (num) on (obj) = 121, lambda: todo()
    # spells: have (obj) cast free and unresistable spell (num) on (obj) = 122, lambda: todo()
    # touch art (num) = 123, lambda: todo()
    # script eye candy: stop (num) on (obj) = 124, lambda: todo()
    # remove from time queue the call to script (num) with attachee (obj) = 125, lambda: todo()
    # destroy item named (num) in inventory of (obj) = 126, lambda: todo()
    # toggle item (obj) inventory display on/off = 127, lambda: todo()
    # heal (obj) for (num) poison points = 128, lambda: todo()
    # schematic UI start: display for (obj) = 129, lambda: todo()
    # spells: stop spell (num) on (obj) = 130, lambda: todo()
    # slideshow: queue slide (num) = 131, lambda: todo()
    # end game and play slides = 132, lambda: todo()
    # rotation of (obj): set to (num) = 133, lambda: todo()
    # faction of npc (obj): set to (num) = 134, lambda: todo()
    # drain (num) charges from (obj) = 135, lambda: todo()
    # spells: cast unresistable spell (num) on (obj) = 136, lambda: todo()
    # stat (num) of (obj): adjust by (num) = 137, lambda: todo()
    # damage (obj) unresistably for (num) points of type (num) damage = 138, lambda: todo()
    # autolevel scheme for (obj): change to (num) = 139, lambda: todo()
    # set day standpoint of critter (obj) to X:(num) Y:(num) on map (num) = 140, lambda: todo()
    # set night standpoint of critter (obj) to X:(num) Y:(num) on map (num) = 141, lambda: todo()


class Condition(FunctionEnum):
    """Enum class of conditions that are used decide the action to execute on a
    given line.

    All functions return a boolean.
    """
    true = 0, lambda: True
    is_daytime = 1, lambda: todo()
    has_gold = 2, lambda target, gold: todo()
    local_flag = 3, lambda flag, script=None: script.flags[flag]
    num_eq = 4, lambda num_1, num_2: num_1 == num_2
    num_le = 5, lambda num_1, num_2: num_1 <= num_2
    pc_quest_has_state = 6, lambda pc, quest_id, state: todo()
    global_quest_has_state = 7, lambda quest_id, state: todo()
    has_blessing = 8, lambda target, blessing_id: todo()
    has_curse = 9, lambda target, curse_id: todo()
    has_met_npc = 10, lambda npc, pc: todo()
    has_bad_associates = 11, lambda target: todo()
    is_polymorphed = 12, lambda target: todo()
    is_shrunk = 13, lambda target: todo()
    has_a_body_spell = 14, lambda target: todo()
    is_invisible = 15, lambda target: todo()
    has_mirror_image = 16, lambda target: todo()
    has_item = 17, lambda target, item_name_id: todo()
    is_follower = 18, lambda npc, pc: todo()
    is_species = 19, lambda npc, species_id: todo()
    is_named = 20, lambda target, name_id: todo()
    is_wielding_item = 21, lambda target, item_name_id: todo()
    is_dead = 22, lambda target: todo()
    has_maximum_followers = 23, lambda target: todo()
    can_open_container = 24, lambda target, container: todo()
    has_surrendered = 25, lambda target: todo()
    is_in_dialog = 26, lambda target: todo()
    is_switched_off = 27, lambda target: todo()
    can_see_object = 28, lambda target, object: todo()
    can_hear_object = 29, lambda target, object: todo()
    is_invulnerable = 30, lambda target: todo()
    is_in_combat = 31, lambda target: todo()
    is_at_location = 32, lambda target, x, y: todo()
    has_reputation = 33, lambda target, reputation_id: todo()
    is_within_n_tiles_of_location = 34, lambda target, n_tiles, x, y: todo()
    is_under_the_influence_of_spell = 35, lambda target, spell_id: todo()
    is_open = 36, lambda target: todo()
    is_an_animal = 37, lambda target: todo()
    is_undead = 38, lambda target: todo()
    was_jilted_by_a_pc = 39, lambda target: todo()
    pc_knows_rumor = 40, lambda pc, rumor_id: todo()
    rumor_has_been_quelled = 41, lambda rumor_id: todo()
    is_busted = 42, lambda target: todo()
    global_flag = 43, lambda flag: todo()
    can_open_portal = 44, lambda target, portal, direction: todo()
    sector_is_blocked = 45, lambda x, y: todo()
    monster_generator_is_disabled = 46, lambda generator_id: todo()
    is_identified = 47, lambda target: todo()
    knows_spell = 48, lambda target, spell_id: todo()
    has_mastered_spell_college = 49, lambda target, spell_id: todo()
    items_are_being_rewielded = 50, lambda: todo()
    is_prowling = 51, lambda target: todo()
    is_waiting = 52, lambda target: todo()
