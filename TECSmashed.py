import time
import re
import random
import sys
from Action import Action

import Combat
import TECHandler
from pickpocketing import pickpocketing


class TECSmashed:
    def __init__(self, filename, windowname):

        self.TECH = TECHandler
        window = self.TECH.get_whndl(windowname)
        self.pycwnd = self.TECH.make_pycwnd(window)
        logfile = open(filename, "r")
        self.combat = Combat.combat(self)
        self.pickpocketing = pickpocketing(self)
        self.directions = ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw']
        self.rotation = ['zz', 'zx', 'zc', 'zv', 'zb', 'zn', 'za', 'za', 'zs']
        # rotation = ['zzh', 'zxh', 'zch', 'zvh', 'zbh', 'znh', 'zmh', 'za', 'zsh']
        self.rollPattern = re.compile('Success: (\d+), Roll: (\d+)')
        self.matchPattern = re.compile('\d\.')
        self.free = True
        self.action_status = False
        self.in_combat = False
        self.palming = False

        self.last_direction = "n"
        self.last_cmd = ""
        self.corpse = 1
        self.next_action = []
        self.current_action = Action.nothing

        loglines = TECHandler.follow(logfile)
        for newLine in loglines:
            self.match_line(newLine)


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


    # Repeats until we run out of corpses.
    def skin(self):
        cmd = "skin" + ( " " if self.corpse == 1 else " " + str(self.corpse) + " ") + "corp"
        self.send_cmd(cmd)
        self.add_action(Action.skin)


    def move_last_direction(self):
        self.send_cmd(self.last_direction)


    def set_trap(self):
        # If the last action
        if self.action_status and self.current_action == (4, Action.set_trap):
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
        self.add_action(Action.skin)


    def dismantle_trap(self):
        self.send_cmd("ds")
        self.free = False


    def perform_action(self):
        # get the last item in the list/highest priority
        if self.free and len(self.next_action) > 0:
            self.current_action = self.next_action.pop()
            print(self.current_action)
            if self.current_action == Action.skin:
                self.free = False
                self.skin()
            elif self.current_action == Action.group_corp:
                self.free = False
                self.send_cmd("group all corpse")
            elif self.current_action == Action.group_junk:
                self.free = False
                self.send_cmd("groupJunk")
            elif self.current_action == Action.group_value:
                self.free = False
                self.send_cmd("groupValue")
            elif self.current_action == Action.set_trap:
                self.set_trap()
            elif self.current_action == Action.look_trap:
                self.look_trap()
            elif self.current_action == Action.dismantle_trap:
                self.dismantle_trap()
            elif self.current_action == Action.release_trap:
                self.release_trap()
            elif self.current_action == Action.repeat:
                if Action.attack not in self.next_action:
                    self.send_cmd(self.last_cmd)
            elif self.current_action == Action.get_parts:
                self.free = False
                self.send_cmd("get parts")


    # def handle_action(self, line):
    #     me = True
    #     if "] A" in line or "] An" in line:
    #         self.add_action(Action.attack)
    #         me = False
    #         if self.free:
    #             print("Free, starting attack")
    #             self.perform_action()
    #     elif "You slit" in line:
    #         print("Killed")
    #         self.add_action(Action.skin)
    #     roll = self.rollPattern.search(line)
    #     if me:
    #         self.action_status = int(roll.group(1)) < int(roll.group(2))


    def handle_set_trap(self):
        action = (4, Action.set_trap)
        if self.current_action != Action.set_trap and action not in self.next_action:
            self.add_action(action)





    def handle_trap(self, line):
        if "but nothing is trapped inside" in line or "rendering it useless" in line:
            print("Dismantle snare")
            self.add_action(Action.dismantle_trap)
            self.free = True
            self.perform_action()
        elif "is trapped inside" in line or "fallen in" in line:
            print("Release snare")
            self.add_action(Action.release_trap)
            self.free = True
            self.perform_action()
        else:
            self.handle_set_trap()
            self.action_status = True
            self.perform_action()


    def match_line(self, line):

        if self.in_combat:
            self.combat.handle_combat_line(line)
        elif self.palming:
            self.pickpocketing.handle_pickpocket_line(line)
        elif "] A" in line or "] An" in line:
            self.in_combat = True
        elif "palm den" in line:
            self.palming = True
        elif "retreat" in line and "You retreat." not in line and "retreat first" not in line and "retreats." not in line:
            self.add_action(Action.retreat)
        # elif "You fumble!" in line:
        #     self.handle_recover(True)
        # elif "You must be wielding a weapon to attack." in line or "You can't do that right now." in line:
        #     self.handle_recover(False)
        # elif "falls unconscious" in line:
        #     print("Unconscious")
        #     self.remove_action(Action.attack)
        #     self.add_action(Action.kill)
        elif "There isn't anything worth skinning on it" in line or "You can only skin corpses." in line:
            self.corpse += 1
            print("Corpse: " + str(self.corpse))
            self.free = True
            self.perform_action()
        elif "skin corpse" in line:
            self.add_action(Action.skin)
            print("Skinning")
        # elif "expires." in line:
        #     self.remove_action(Action.kill)
        #     self.add_action(Action.skin)
        #     print("Dead")
        #     self.free = True
        elif "There aren't that many here." in line:
            print("Stop Skinning")
            self.remove_action(Action.skin)
            if self.corpse > 2:
                self.add_action(Action.group_corp)
            self.add_action(Action.get_parts)
            self.add_action(Action.group_value)
            # self.add_action((7, Action.group_junk))
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
            self.current_action = Action.nothing
            self.free = True
            time.sleep(random.randrange(1234, 2512) / 1000)
            self.handle_set_trap()
            self.perform_action()
        elif "You are in the middle of something." in line or "You will be busy for" in line:
            print("Repeating: " + self.last_cmd)
            self.add_action(Action.repeat)
            self.free = True
            self.perform_action()
        elif "This crude snare is" in line:
            self.handle_trap(line)
        elif "You don't see a \"snare\" here." in line:
            self.handle_set_trap()
            self.perform_action()
        elif "There is already a trap in this area" in line:
            print("look snare")
            self.action_status = True
            self.free = True
            self.add_action(Action.look_trap)
            self.perform_action()
        elif "sstat" in line:
            print(self.next_action)
            print(self.last_direction)


if __name__ == '__main__':
    TECSmashed(sys.argv[1], sys.argv[2])
