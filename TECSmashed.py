from enum import Enum
import time
import re
import random

import TECHandler


class Action(Enum):
    nothing = 0
    attack = 1
    recover = 2
    wield = 3
    skin = 4
    kill = 5
    group_corp = 6
    group_junk = 7
    group_value = 8
    get_value = 9
    set_trap = 10
    dismantle_trap = 11
    repeat = 12
    look_trap = 13
    release_trap = 14
    retreat = 15


directions = ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw']

rotation = ['zz', 'zx', 'zc', 'zv', 'zb', 'zn', 'za', 'za', 'zs']
# rotation = ['zzh', 'zxh', 'zch', 'zvh', 'zbh', 'znh', 'zmh', 'za', 'zsh']
rollPattern = re.compile('Success: (\d+), Roll: (\d+)')
matchPattern = re.compile('\d\.')
free = True
action_status = False

last_direction = "n"
last_cmd = ""
corpse = 1
next_action = []
current_action = (0, Action.nothing)


def send_cmd(cmd):
    global last_cmd
    last_cmd = cmd
    time.sleep(random.randrange(567, 2209) / 1000.0)
    print(cmd)
    TEC.send_cmd(pycwnd, cmd)


def add_action(action):
    if action not in next_action:
        next_action.append(action)
        next_action.sort()
        print("Add: " + str(next_action))


def remove_action(action):
    if action in next_action:
        next_action.remove(action)
        next_action.sort()
        print("Remove: " + str(next_action))


# Repeats until we kill something
def attack():
    index = random.randrange(0, 8)
    cmd = rotation[index]
    send_cmd(cmd)
    add_action((10, Action.attack))


# Repeats until we run out of corpses.
def skin():
    cmd = "skin" + ( " " if corpse == 1 else " " + str(corpse) + " ") + "corp"
    send_cmd(cmd)
    add_action((9, Action.skin))


def move_last_direction():
    send_cmd(last_direction)


def set_trap():
    global free, action_status
    if action_status:
        move_last_direction()
        time.sleep(random.randrange(1234, 2512) / 1000)
        action_status = False
        handle_set_trap()
        perform_action()
    else:
        free = False
        send_cmd("sd")


def look_trap():
    send_cmd("l snare")


def release_trap():
    send_cmd("release snare")
    send_cmd("kill")
    add_action((9, Action.skin))


def dismantle_trap():
    global free
    send_cmd("ds")
    free = False


def recover():
    global free
    free = False
    send_cmd("get dag")
    time.sleep(random.randrange(1234, 2512) / 1000)
    send_cmd("wie dag")
    free = True


def perform_action():
    global last_cmd, free, current_action
    # get the last item in the list/highest priority
    if free and len(next_action) > 0:
        current_action = next_action.pop()
        print(current_action)
        if current_action[1] == Action.recover:
            recover()
        elif current_action[1] == Action.retreat:
            free = False
        elif current_action[1] == Action.kill:
            free = False
            send_cmd("kl")
        elif current_action[1] == Action.attack:
            free = False
            attack()
        elif current_action[1] == Action.skin:
            free = False
            skin()
        elif current_action[1] == Action.group_corp:
            free = False
            send_cmd("group all corpse")
        elif current_action[1] == Action.group_junk:
            free = False
            send_cmd("groupJunk")
        elif current_action[1] == Action.group_value:
            free = False
            send_cmd("groupValue")
        elif current_action[1] == Action.set_trap:
            set_trap()
        elif current_action[1] == Action.look_trap:
            look_trap()
        elif current_action[1] == Action.dismantle_trap:
            dismantle_trap()
        elif current_action[1] == Action.release_trap:
            release_trap()
        elif current_action[1] == Action.repeat:
            if (10, Action.attack) not in next_action:
                send_cmd(last_cmd)
                # elif get_parts:
                # free = False
                # grouping = False
                # send_cmd("get parts")
                # send_cmd("get parts")


def handle_action(line):
    global recovering, action_status, free, corpse
    me = True
    if "] A" in line or "] An" in line:
        add_action((10, Action.attack))
        me = False
        if free:
            print("Free, starting attack")
            perform_action()
    elif "You slit" in line:
        print("Killed")
        add_action((9, Action.skin))
    roll = rollPattern.search(line)
    if me:
        action_status = int(roll.group(1)) < int(roll.group(2))


def handle_set_trap():
    action = (5, Action.set_trap)
    if current_action != Action.set_trap and action not in next_action:
        add_action(action)


def handle_recover(wait):
    add_action((1000, Action.recover))
    if wait:
        perform_action()


def handle_trap(line):
    global free
    if "but nothing is trapped inside" in line:
        print("Dismantle snare")
        add_action((9, Action.dismantle_trap))
        free = True
        perform_action()
    elif "is trapped inside" in line or "fallen in" in line:
        print("Release snare")
        add_action((7, Action.release_trap))
        free = True
        perform_action()
    else:
        handle_set_trap()


def handle_line(line):
    global action_status, last_cmd, last_direction, free, corpse, get_parts
    if line[0] == "[":
        handle_action(line)
    elif "retreat" in line and "You retreat." not in line:
        add_action((999, Action.retreat))
    elif "You fumble!" in line:
        handle_recover(True)
    elif "You must be wielding a weapon to attack." in line or "You can't do that right now." in line:
        handle_recover(False)
    elif "falls unconscious" in line:
        print("Unconscious")
        remove_action((10, Action.attack))
        add_action((11, Action.kill))
    elif "There isn't anything worth skinning on it" in line or "You can only skin corpses." in line:
        corpse += 1
        print("Corpse: " + str(corpse))
        free = True
        perform_action()
    elif "skin corpse" in line:
        add_action((9, Action.skin))
        print("Skinning")
    elif "expires." in line:
        remove_action((11, Action.kill))
        add_action((9, Action.skin))
        print("Dead")
        free = True
    elif "There aren't that many here." in line:
        print("Stop Skinning")
        remove_action((9, Action.skin))
        if corpse > 2:
            add_action((8, Action.group_corp))
            add_action((6, Action.group_value))
        add_action((7, Action.group_junk))
        corpse = 1
        free = True
        perform_action()
    elif "You are already carrying an" in line and "animal parts" in line:
        free = True
    elif line.strip() == "You are no longer busy.":
        print("Not Busy")
        free = True
        perform_action()
    elif line.strip() in directions:
        last_direction = line.strip()
        free = True
    elif "sd" == line:
        print("Starting trapping")
        handle_set_trap()
    elif "The ground is too soft and loose to dig" in line:
        move_last_direction()
        handle_set_trap()
        perform_action()
    elif "You are in the middle of something." in line or "You will be busy for" in line:
        print("Repeating: " + last_cmd)
        add_action((1000, Action.repeat))
        free = True
        perform_action()
    elif "This crude snare is" in line:
        handle_trap(line)
    elif "There is already a trap in this area" in line:
        print("look snare")
        action_status = True
        free = True
        add_action((8, Action.look_trap))
        perform_action()
    elif "sstat" in line:
        print(next_action)
        print(last_direction)


if __name__ == '__main__':

    TEC = TECHandler
    window = TEC.get_whndl()
    pycwnd = TEC.make_pycwnd(window)
    logfile = open("P:/tec.txt", "r")
    loglines = TECHandler.follow(logfile)
    for newLine in loglines:
        handle_line(newLine)

