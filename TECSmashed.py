import os
import time
import random
from tkinter import *

from Action import Action
import combat
import TECHandler
from pickpocketing import pickpocketing


class TECSmashed:
    def __init__(self, filename, windowname):

        self.TECH = TECHandler
        window = self.TECH.get_whndl(windowname)
        self.pycwnd = self.TECH.make_pycwnd(window)
        self.filename = filename
        self.file = open(self.filename, "r")
        self.combat = combat.combat(self)
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
        self.paused = False

        self.last_direction = "n"
        self.last_cmd = ""
        self.corpse = 1
        self.queue = []
        self.current_action = Action.nothing
        self.data = self.file.read()
        self.size = len(self.data)
        self.top = Tk()
        self.poll()
        self.pause_button = Button(self.top, text="Pause", command=self.toggle_pause)
        self.reset_button = Button(self.top, text="Reset Queue", command=self.reset_queue)
        self.reset_button.pack()
        self.pause_button.pack()
        self.top.mainloop()

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button["text"] = "Run" if self.paused else "Pause"

    def reset_queue(self):
        self.queue = []

    def poll(self):
        if os.path.getsize(self.filename) > self.size:
            line = self.file.read()
            self.size += len(line)
            if not self.paused:
                self.match_line(line)
        self.top.after(100, self.poll)

    def parse_line(self, file, top):
        line = TECHandler.get_line(file)
        print(line)
        self.match_line(line)
        top.after(100, self.parse_line, file, top)

    def send_cmd(self, cmd):
        self.last_cmd = cmd
        time.sleep(random.randrange(567, 4209) / 1000.0)
        print(cmd)
        self.TECH.send_input(self.pycwnd, cmd)
        # randomly double send
        if random.randrange(1, 15) == 1:
            time.sleep(random.randrange(567, 1209) / 1000.0)
            self.TECH.send_input(self.pycwnd, cmd)


    def add_action(self, action):
        if action not in self.queue:
            self.queue.append(action)
            self.queue.sort()
            print("Add: " + str(self.queue))


    def remove_action(self, action):
        if action in self.queue:
            self.queue.remove(action)
            self.queue.sort()
            print("Remove: " + str(self.queue))


    # Repeats until we run out of corpses.
    def skin(self):
        cmd = "skin" + ( " " if self.corpse == 1 else " " + str(self.corpse) + " ") + "corp"
        self.send_cmd(cmd)
        self.add_action(Action.skin)

    def move_last_direction(self):
        self.send_cmd(self.last_direction)

    def set_trap(self):
        # If the last action
        if self.action_status and self.current_action == Action.set_trap:
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
        self.free = True

    def release_trap(self):
        self.send_cmd("release snare")
        self.send_cmd("kill")
        self.add_action(Action.skin)


    def dismantle_trap(self):
        self.send_cmd("ds")
        self.free = False


    def perform_action(self):
        # get the last item in the list/highest priority
        if self.free and len(self.queue) > 0:
            self.current_action = self.queue.pop()
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
            elif self.current_action == Action.cast_pole:
                self.free = False
                self.add_action(Action.cast_pole)
                self.send_cmd("cast pole")
            elif self.current_action == Action.repeat:
                if Action.attack not in self.queue:
                    self.send_cmd(self.last_cmd)
            elif self.current_action == Action.get_parts:
                self.free = False
                self.send_cmd("get parts")


    # def handle_action(self, line):
    # me = True
    # if "] A" in line or "] An" in line:
    # self.add_action(Action.attack)
    # me = False
    # if self.free:
    # print("Free, starting attack")
    # self.perform_action()
    # elif "You slit" in line:
    # print("Killed")
    # self.add_action(Action.skin)
    # roll = self.rollPattern.search(line)
    # if me:
    # self.action_status = int(roll.group(1)) < int(roll.group(2))


    def handle_set_trap(self):
        action = Action.set_trap
        if self.current_action != Action.set_trap and action not in self.queue:
            self.add_action(action)


    def handle_trap(self, line):
        if "but nothing is trapped inside" in line or "rendering it useless" in line:
            print("Dismantle snare")
            self.add_action(Action.set_trap)
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
        if "You are no longer busy" in line:
            print("Not Busy")
            self.free = True
            self.perform_action()
        elif self.in_combat:
            self.combat.handle_combat_line(line)
        elif self.palming:
            self.pickpocketing.handle_pickpocket_line(line)
        # elif self.hunting:
        #     self.hunting_lore.handle_hunting_line(line)
        elif ( "] A" in line or "] An" in line) and "You retrieve the line" not in line:
            print("Combat")
            print(line)
            self.in_combat = True
        elif "p" == line or "o" == line or "m" == line:
            print("Pickpocketing")
            self.palming = True
        elif "retreat" in line and "You retreat." not in line and "retreat first" not in line and "retreats." not in line:
            print("Retreating")
            self.add_action(Action.retreat)
        elif "There isn't anything worth skinning on it" in line or "You can only skin corpses." in line:
            self.corpse += 1
            print("Corpse: " + str(self.corpse))
            self.free = True
            self.perform_action()
        elif "skin corpse" in line:
            print("Skinning")
            self.add_action(Action.skin)
        elif "There aren't that many here." in line:
            print("Stop Skinning")
            self.remove_action(Action.skin)
            if self.corpse > 2:
                self.add_action(Action.group_corp)
            self.corpse = 1
            self.free = True
            self.perform_action()
        elif "You are already carrying an" in line and "animal parts" in line:
            self.free = True
        elif line.strip() in self.directions:
            self.last_direction = line.strip()
            print("Changing directions")
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
        elif "You are in the middle of something." in line:  # or "You will be busy for" in line:
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
        elif "cast pole" in line:
            self.add_action(Action.cast_pole)
        elif "sstat" in line:
            print(self.queue)
            print("Free: " + self.free)
            print(self.last_direction)


if __name__ == '__main__':
    TECSmashed(sys.argv[1], sys.argv[2])
