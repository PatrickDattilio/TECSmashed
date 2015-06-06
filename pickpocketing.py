from threading import Timer

from Action import Action


class pickpocketing:
    def __init__(self, tec):
        self.tec = tec
        self.free = False
        self.action = Action.nothing
        self.timer = Timer(3.0, self.perform_action())
        self.last_command = ""
        self.palming = False
        self.looking = False
        self.skip_fade = False
        # self.dock = ['s', 's', 's', 's', 's', 'n', 'n', 'n', 'n', 'n']

        #self.dock = ['s', 's', 's', 's', 's', 'e', 'e', 'e', 'e', 'w', 'w', 'w', 'w', 'n', 'n', 'n', 'n', 'n', 'e', 'e',
         #            'e', 'w', 'w', 'w']
        self.dock = ['n','n','e','e','w','w','s','s','w','w','e','e']
        self.position = 0

    def add_action(self, action):
        if action not in self.tec.queue:
            self.tec.queue.append(action)
            self.tec.queue.sort()
            print("QueueA: " + str(self.tec.queue))


    def remove_action(self, action):
        if action in self.tec.queue:
            self.tec.queue.remove(action)
            self.tec.queue.sort()
            print("QueueD: " + str(self.tec.queue))

    def send_cmd(self, cmd):
        print("Sending: " + cmd)
        self.last_command = cmd
        self.tec.send_cmd(cmd)


    def palm_timeout(self):
        print("Timeout")
        self.add_action(Action.repeat)
        self.free = True
        self.perform_action()

    def retry(self):
        print("Retying command: " + self.last_command)
        self.tec.send_cmd(self.last_command)

    def move(self):
        move = self.dock[self.position % len(self.dock)]
        print("Moving: " + move)
        self.tec.send_cmd(move, 0, "You walk", False)


    def handle_pickpocket_line(self, line):
        if line.strip() == "You are no longer busy." or "You retreat." in line:
            print("P: Not Busy")
            self.free = True
            self.perform_action()
        if "You are in the middle of something." in line:
            self.add_action(Action.repeat)
            self.perform_action()
        elif "You are already palming that." in line:
            print("P: Already palming")
            self.free = True
            self.add_action(Action.unpalm)
            self.perform_action()
        elif "reappear in your hand." in line or "You aren't palming anything" in line:
            print("P:Flip")
            self.timer.cancel()
            self.free = True
            self.add_action(Action.palm)
            self.perform_action()
        elif "spookt" == line:
            self.add_action(Action.spook)
        elif "ect" == line:
            self.add_action(Action.ear)
        elif "p" == line or "o" == line:
            self.palming = True

        elif "You drop" in line:
            self.add_action(Action.get_den)
            self.add_action(Action.palm)
        elif "You spot a trader within the crowd." in line:
            self.add_action(Action.look_at_target)
            self.free = True
            self.looking = True
            self.perform_action()
        # elif "You manage to get right on top of a trader" in line:
        # self.add_action(Action.slice)
        elif "You empty the contents " in line:
            self.add_action(Action.discard)
            self.perform_action()
        elif "Are you sure you want to throw" in line:
            self.add_action(Action.confirm)
            self.perform_action()
        elif "You discard a" in line:
            if self.skip_fade:
                self.skip_fade = False
            else:
                self.add_action(Action.fade)
            self.perform_action()
        elif "You arrive at" in line:
            self.position = self.position + 1;
            if "A trader is here" in line or "trader are here" in line or "A trader is right here." in line:
                print("Move on, occupied")
                self.add_action(Action.move)
                self.perform_action()
            else:
                self.tec.send_cmd("xx", 150, "You spot")
        elif "cut the strap" in line:
            print("Slice successful")
            if "drop" in line:
                self.add_action(Action.get_gems)
            if "move away from a trader" in line:
                print("Skip Fade")
                self.skip_fade = True
            self.add_action(Action.move)
            self.add_action(Action.empty)
        elif "can't seem to find an opening" in line:
            self.add_action(Action.ground_approach)
        elif self.looking and "is wearing" in line:
            self.looking = False
            if "mesh" in line or "tan linen" in line or "crude" in line or "reddish" in line or "bag" in line or "neck" in line or "box" in line or "fur" in line or "tiny" in line or "tube" in line or "sack" in line or "backpack" in line:
                print("Should approach")
                self.add_action(Action.slice)
                self.add_action(Action.ground_approach)
                self.perform_action()
            else:
                print("Move on")
                self.add_action(Action.move)
                self.perform_action()
        elif "[Success:" in line:
            self.timer.cancel()
            roll = self.tec.rollPattern.search(line)
            # Successsful action
            if int(roll.group(1)) < int(roll.group(2)):
                if self.palming:
                    self.add_action(Action.unpalm)
            else:
                if self.palming:
                    self.add_action(Action.palm)

    def perform_action(self):
        if self.free and len(self.tec.queue) > 0:
            self.action = self.tec.queue.pop()
            if self.action == Action.palm:
                self.free = False
                self.tec.send_cmd("p", 5000, "You")
            elif self.action == Action.unpalm:
                self.tec.send_cmd("o", 5000, "You")
                self.perform_action()
            elif self.action == Action.get_den:
                self.tec.send_cmd("get den")
                self.perform_action()
            elif self.action == Action.spook:
                self.add_action(Action.spook)
                self.tec.send_cmd("spookt")
            elif self.action == Action.ear:
                self.add_action(Action.ear)
                self.tec.send_cmd("ect")
            elif self.action == Action.repeat:
                self.retry()
            elif self.action == Action.move:
                self.move()
            elif self.action == Action.look_at_target:
                self.tec.send_cmd("xc", 225, "You see a")
            elif self.action == Action.ground_approach:
                self.tec.send_cmd("xv", 305, "[Success")
            elif self.action == Action.slice:
                self.tec.send_cmd("xb", 100, "[Success")
            elif self.action == Action.empty:
                self.tec.send_cmd("xn", 340, "You empty")
            elif self.action == Action.get_gems:
                self.tec.send_cmd("xg", 0, "You take a")
                self.perform_action()
            elif self.action == Action.discard:
                self.tec.send_cmd("xm", 75, "Are you sure", False)
            elif self.action == Action.confirm:
                self.tec.send_cmd("y", 0, "You discard")
            elif self.action == Action.fade:
                self.tec.send_cmd("x,", 254, "[Success")


