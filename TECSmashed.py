from enum import Enum
import time
import re
import random
import win32gui
import win32ui
import queue

import win32con


class Action(Enum):
    attack = 1
    recover = 2
    wield = 3
    skin = 4
    kill = 5
    groupCorp = 6
    group_junk = 7
    group_value = 8
    get_value = 9


rotation = ['zz', 'zx', 'zc', 'zv', 'zb', 'zn', 'za', 'za', 'zs']
# rotation = ['zzh', 'zxh', 'zch', 'zvh', 'zbh', 'znh', 'zmh', 'za', 'zsh']
rollPattern = re.compile('Success: (\d+), Roll: (\d+)')
matchPattern = re.compile('\d\.')
recovering = False
wielding = False
attacking = False
free = True
skinning = False
killing = False
cleanup = False
grouping = False
get_parts = False
corpse = 1

next_action = []

def add_action(action):
    next_action.append(action)
    next_action.sort()

def f_click(pycwnd):
    x = 167
    y = 844

def get_whndl():
    whndl = win32gui.FindWindowEx(0, 0, None, 'TEC - Mozilla Firefox')
    return whndl


def make_pycwnd(hwnd):
    PyCWnd = win32ui.CreateWindowFromHandle(hwnd)
    return PyCWnd


def send_input(msg):
    time.sleep(random.randrange(567, 2209) / 1000.0)
    print(msg)
    f_click(pycwnd)
    for c in msg:
        if c == "\n":
            pycwnd.SendMessage(win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            pycwnd.SendMessage(win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            pycwnd.SendMessage(win32con.WM_CHAR, ord(c), 0)
    pycwnd.SendMessage(win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    pycwnd.SendMessage(win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    pycwnd.UpdateWindow()


whndl = get_whndl()


def callback(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        hwnds[win32gui.GetClassName(hwnd)] = hwnd
    return True


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def attack():
    index = random.randrange(0, 8)
    cmd = rotation[index]
    send_input(cmd)


def skin():
    cmd = "skin" + ( " " if corpse == 1 else " " + str(corpse) + " ") + "corp"
    send_input(cmd)


def perform_action():
    #get the last item in the list/highest priority
    action = next_action.pop()
    global recovering, wielding, attacking, free, skinning, corpse, killing, cleanup, grouping, get_parts
    if recovering:
        free = False
        send_input("get dag")
        time.sleep(random.randrange(1234, 2512) / 1000)
        send_input("wie dag")
        free = True
        recovering = False
        attacking = True
    elif killing:
        free = False
        send_input("kl")
    elif attacking:
        free = False
        attack()
    elif skinning:
        free = False
        skin()
    elif cleanup:
        free = False
        cleanup = False
        grouping = True
        send_input("group all corpse")
    elif grouping:
        free = False
        grouping = False
        #get_parts = True
        send_input("groupIsland")
        # elif get_parts:
        #     free = False
        #     grouping = False
        #     send_input("get parts")
        #     send_input("get parts")


def handle_action(line):
    global recovering, wielding, attacking, free, skinning, corpse, killing, cleanup, grouping, get_parts
    me = True
    if "] A" in line or "] An" in line:
        attacking = True
        me = False
        if free:
            print("Free, starting attack")
            perform_action()
    elif "You slit" in line:
        print("Killed")
        skinning = True
        killing = False
    roll = rollPattern.search(line)
    if int(roll.group(1)) < int(roll.group(2)):
        print(("I " if me else "They ") + "Hit!");
    else:
        print(("I " if me else "They ") + "Miss")


def handle_line(line):
    global recovering, wielding, attacking, free, skinning, corpse, killing, cleanup, grouping, get_parts
    if line[0] == "[":
        handle_action(line)
    elif "You fumble!" in line:
        queue.put((100, Action.recover))
        # print("Recovering weapon")
        # recovering = True
    elif "You must be wielding a weapon to attack." in line or "You can't do that right now." in line:
        queue.put((100, Action.recover))
        # print("Getting weapon")
        # recovering = True
        perform_action()
    elif "falls unconscious" in line:
        print("Unconscious")
        attacking = False
        killing = True
    elif "There isn't anything worth skinning on it" in line or "You can only skin corpses." in line:
        corpse += 1
        print("Corpse: " + str(corpse))
        perform_action()
    elif "skin corpse" in line:
        skinning = True
        print("Skinning")
    elif "expires." in line:
        print("Dead")
        killing = False
        skinning = True
        free = True
    elif "There aren't that many here." in line:
        print("Stop Skinning")
        skinning = False
        if corpse > 2:
            cleanup = True
        corpse = 1
        perform_action()
    elif "You are already carrying an" in line and "animal parts" in line:
        get_parts = False
        free = True
    elif line.strip() == "You are no longer busy.":
        print("Not Busy")
        free = True
        perform_action()
    elif "sstat" in line:
        print("recovering: " + str(recovering))
        print("wielding: " + str(wielding))
        print("attacking: " + str(attacking))
        print("free: " + str(free))
        print("skinning: " + str(skinning))
        print("corpse: " + str(corpse))
        print("killing: " + str(killing))
        # else:
        #print(line)


if __name__ == '__main__':
    hwnds = {}
    pycwnd = make_pycwnd(whndl)
    logfile = open("P:/tec.txt", "r")
    loglines = follow(logfile)
    for line in loglines:
        handle_line(line)

