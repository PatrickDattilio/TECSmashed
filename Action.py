from enum import IntEnum


class Action(IntEnum):
    nothing = 0
    skin = 4
    group_corp = 6
    group_junk = 7
    group_value = 8
    get_value = 9
    set_trap = 10
    dismantle_trap = 11
    repeat = 1000
    look_trap = 13
    release_trap = 14
    get_parts = 16
    cast_pole = 17
    ###


    ##### Pickpocketing aciongs
    palm = 40
    unpalm = 41
    get_den = 42

    ###### Combat actions
    combat_skin = 50
    attack = 51
    kill = 52
    release = 53
    wield = 54
    get_weapon = 55
    retreat = 56
    recover = 57