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
    find_twig = 35
    make_rope = 36

    ##### Pickpocketing aciongs
    palm = 40
    unpalm = 41
    get_den = 42
    spook = 43
    ear = 44
    move = 45
    look_for_target = 46
    look_at_target = 47
    slice = 48
    ground_approach = 49
    empty = 50
    get_gems = 51
    fade = 52
    discard = 53
    confirm = 54

    ###### Combat actions
    attack = 60
    combat_skin = 61
    kill = 62
    release = 63
    wield = 64
    get_weapon = 65
    retreat = 66
    recover = 67

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