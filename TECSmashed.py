from enum import Enum
import time
import re
import random
import Combat

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
    # combat_skin = 50
    # attack = 51
    # kill = 52
    # wield = 53
    # get_weapon = 54
    # retreat = 55


class TECSmashed:


    def __init__(self):
        self.TECH = TECHandler
        window = self.TECH.get_whndl()
        self.pycwnd = self.TECH.make_pycwnd(window)
        logfile = open("P:/tec.txt", "r")
        self.combat = Combat.combat(self)
        self.directions = ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw']
        self.rotation = ['zz', 'zx', 'zc', 'zv', 'zb', 'zn', 'za', 'za', 'zs']
        # rotation = ['zzh', 'zxh', 'zch', 'zvh', 'zbh', 'znh', 'zmh', 'za', 'zsh']
        self.rollPattern = re.compile('Success: (\d+), Roll: (\d+)')
        self.matchPattern = re.compile('\d\.')
        self.free = True
        self.action_status = False
        self.in_combat = False

        self.last_direction = "n"
        self.last_cmd = ""
        self.corpse = 1
        self.next_action = []
        self.current_action = (0, Action.nothing)

        loglines = TECHandler.follow(logfile)
        for newLine in loglines:
            self.handle_line(newLine)


    def send_cmd(self, cmd):
        self.last_cmd = cmd
        time.sleep(random.randrange(567, 2209) / 1000.0)
        print(cmd)
        self.TECH.send_input(self.pycwnd, cmd)


    def add_action(self, action):
        if action not in self.next_action:
            self.next_action.append(action)
            self.next_action.sort()
            print("Add: " + str(self.next_action))


    def remove_action(self, action):
        if action in self.next_action:
            self.next_action.remove(action)
            self.next_action.sort()
            print("Remove: " + str(self.next_action))


    # Repeats until we kill something
    def attack(self):
        index = random.randrange(0, 8)
        cmd = self.rotation[index]
        self.send_cmd(cmd)
        self.add_action((10, Action.attack))


    # Repeats until we run out of corpses.
    def skin(self):
        cmd = "skin" + ( " " if self.corpse == 1 else " " + str(self.corpse) + " ") + "corp"
        self.send_cmd(cmd)
        self.add_action((9, Action.skin))


    def move_last_direction(self):
        self.send_cmd(self.last_direction)


    def set_trap(self):
        if self.action_status:
            self.move_last_direction()
            time.sleep(random.randrange(1234, 2512) / 1000)
            self.action_status = False
            self.handle_set_trap()
            self.perform_action()
        else:
            self.free = False
            self.send_cmd("sd")


    def look_trap(self):
        self.send_cmd("l snare")


    def release_trap(self):
        self.send_cmd("release snare")
        self.send_cmd("kill")
        self.add_action((9, Action.skin))


    def dismantle_trap(self):
        self.send_cmd("ds")
        self.free = False


    def recover(self):
        self.free = False
        self.send_cmd("get dag")
        time.sleep(random.randrange(1234, 2512) / 1000)
        self.send_cmd("wie dag")
        self.free = True


    def perform_action(self):
        # get the last item in the list/highest priority
        if self.free and len(self.next_action) > 0:
            self.current_action = self.next_action.pop()
            print(self.current_action)
            if self.current_action[1] == Action.recover:
                self.recover()
            elif self.current_action[1] == Action.retreat:
                self.free = False
            elif self.current_action[1] == Action.kill:
                self.free = False
                self.send_cmd("kl")
            elif self.current_action[1] == Action.attack:
                self.free = False
                self.attack()
            elif self.current_action[1] == Action.skin:
                self.free = False
                self.skin()
            elif self.current_action[1] == Action.group_corp:
                self.free = False
                self.send_cmd("group all corpse")
            elif self.current_action[1] == Action.group_junk:
                self.free = False
                self.send_cmd("groupJunk")
            elif self.current_action[1] == Action.group_value:
                self.free = False
                self.send_cmd("groupValue")
            elif self.current_action[1] == Action.set_trap:
                self.set_trap()
            elif self.current_action[1] == Action.look_trap:
                self.look_trap()
            elif self.current_action[1] == Action.dismantle_trap:
                self.dismantle_trap()
            elif self.current_action[1] == Action.release_trap:
                self.release_trap()
            elif self.current_action[1] == Action.repeat:
                if (10, Action.attack) not in self.next_action:
                    self.send_cmd(self.last_cmd)
                    # elif get_parts:
                    # self.free = False
                    # grouping = False
                    # send_cmd("get parts")
                    # send_cmd("get parts")


    def handle_action(self, line):
        me = True
        if "] A" in line or "] An" in line:
            self.add_action((10, Action.attack))
            me = False
            if self.free:
                print("Free, starting attack")
                self.perform_action()
        elif "You slit" in line:
            print("Killed")
            self.add_action((9, Action.skin))
        roll = self.rollPattern.search(line)
        if me:
            self.action_status = int(roll.group(1)) < int(roll.group(2))


    def handle_set_trap(self):
        action = (5, Action.set_trap)
        if self.current_action != Action.set_trap and action not in self.next_action:
            self.add_action(action)


    def handle_recover(self, wait):
        self.add_action((1000, Action.recover))
        if wait:
            self.perform_action()


    def handle_trap(self, line):
        if "but nothing is trapped inside" in line or "rendering it useless" in line:
            print("Dismantle snare")
            self.add_action((9, Action.dismantle_trap))
            self.free = True
            self.perform_action()
        elif "is trapped inside" in line or "fallen in" in line:
            print("Release snare")
            self.add_action((7, Action.release_trap))
            self.free = True
            self.perform_action()
        else:
            self.handle_set_trap()
            self.perform_action()


    def handle_line(self, line):

        # if in_combat:
        #     self.combat.handle_combat_line(line)
        #
        # if "] A" in line or "] An" in line:
        # in_combat = True

        if line[0] == "[":
            self.handle_action(line)
        elif "retreat" in line and "You retreat." not in line and "retreat first" not in line and "retreats." not in line:
            self.add_action((999, Action.retreat))
        elif "You fumble!" in line:
            self.handle_recover(True)
        elif "You must be wielding a weapon to attack." in line or "You can't do that right now." in line:
            self.handle_recover(False)
        elif "falls unconscious" in line:
            print("Unconscious")
            self.remove_action((10, Action.attack))
            self.add_action((11, Action.kill))
        elif "There isn't anything worth skinning on it" in line or "You can only skin corpses." in line:
            self.corpse += 1
            print("Corpse: " + str(self.corpse))
            self.free = True
            self.perform_action()
        elif "skin corpse" in line:
            self.add_action((9, Action.skin))
            print("Skinning")
        elif "expires." in line:
            self.remove_action((11, Action.kill))
            self.add_action((9, Action.skin))
            print("Dead")
            self.free = True
        elif "There aren't that many here." in line:
            print("Stop Skinning")
            self.remove_action((9, Action.skin))
            if self.corpse > 2:
                self.add_action((8, Action.group_corp))
                self.add_action((6, Action.group_value))
            self.add_action((7, Action.group_junk))
            self.corpse = 1
            self.free = True
            self.perform_action()
        elif "You are already carrying an" in line and "animal parts" in line:
            self.free = True
        elif line.strip() == "You are no longer busy.":
            print("Not Busy")
            self.free = True
            self.perform_action()
        elif line.strip() in self.directions:
            self.last_direction = line.strip()
            self.free = True
        elif "sd" == line:
            print("Starting trapping")
            self.handle_set_trap()
        elif "The ground is too soft and loose to dig" in line:
            self.move_last_direction()
            self.current_action = (0, Action.nothing)
            self.free = True
            time.sleep(random.randrange(1234, 2512) / 1000)
            self.handle_set_trap()
            self.perform_action()
        elif "You are in the middle of something." in line or "You will be busy for" in line:
            print("Repeating: " + self.last_cmd)
            self.add_action((1000, Action.repeat))
            self.free = True
            self.perform_action()
        elif "This crude snare is" in line:
            self.handle_trap(line)
        elif "There is already a trap in this area" in line:
            print("look snare")
            self.action_status = True
            self.free = True
            self.add_action((8, Action.look_trap))
            self.perform_action()
        elif "sstat" in line:
            print(self.next_action)
            print(self.last_direction)

if __name__ == '__main__':
    TECSmashed()