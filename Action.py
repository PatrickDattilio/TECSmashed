from enum import IntEnum


class Action(IntEnum):
    nothing = 0
    #attack = 1
    recover = 2
    #wield = 3
    skin = 4
    #kill = 5
    group_corp = 6
    group_junk = 7
    group_value = 8
    get_value = 9
    set_trap = 10
    dismantle_trap = 11
    repeat = 1000
    look_trap = 13
    release_trap = 14
    #retreat = 999
    get_parts = 16
    # combat_skin = 50
    # attack = 51
    # kill = 52
    # wield = 53
    # get_weapon = 54
    # retreat = 55

    ##### Pickpocketing aciongs
    palm = 40
    unpalm = 41
    get_den = 42

    ###### Combat actions
    combat_skin = 50
    attack = 51
    kill = 52
    wield = 53
    get_weapon = 54
    retreat = 55