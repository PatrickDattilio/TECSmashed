from enum import IntEnum


class Action(IntEnum):
    nothing = 0
    group_corp = 6
    group_junk = 7
    group_value = 8
    get_value = 9
    repeat = 1000
    get_parts = 16
    cast_pole = 17
    bait_pole = 18
    ###


    ##### Hunting Lore
    skin = 4
    release_trap = 24
    look_trap = 20
    set_trap = 10
    dismantle_trap = 11

    ##### Outdoor Basics
    stoke_fire_twig = 30
    find_firewood = 31
    make_torch = 32
    find_grass = 33
    find_berries = 34

    ##### Pickpocketing aciongs
    palm = 40
    unpalm = 41
    get_den = 42
    spook = 43
    ear = 44

    ###### Combat actions
    attack = 50
    combat_skin = 51
    kill = 52
    release = 53
    wield = 54
    get_weapon = 55
    retreat = 56
    recover = 57

    ####Courses
    go_coals = 91
    go_track = 92
    jump_rope = 93
    go_path = 94
    go_plank = 95
    climb_rope = 96
    south = 97
    east = 98
    stand = 99