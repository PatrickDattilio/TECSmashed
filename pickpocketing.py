from threading import Timer
from Action import Action


class pickpocketing:

    def __init__(self, tec):
        self.tec = tec
        self.free = False
        self.queue = []
        self.action = Action.nothing
        self.timer = Timer(3.0, self.perform_action())
        self.last_command = ""


    def add_action(self, action):
        if action not in self.queue:
            self.queue.append(action)
            self.queue.sort()
            print("QueueA: " + str(self.queue))


    def remove_action(self, action):
        if action in self.queue:
            self.queue.remove(action)
            self.queue.sort()
            print("QueueD: " + str(self.queue))

    def send_cmd(self, cmd):
        self.last_command = cmd
        self.tec.send_cmd(cmd)

    def handle_pickpocket_line(self, line):
        print("Pickpocket line: "+line)
        if line.strip() == "You are no longer busy.":
            print("P: Not Busy")
            self.free = True
            self.perform_action()
        elif "You are already palming that." in line:
            print("P: Already palming")
            self.free = True
            self.add_action(Action.unpalm)
            self.perform_action()
        elif "You flip your wrist, and cause a silver denar to reappear in your hand." in line:
            self.free = True
            self.add_action(Action.palm)
            self.perform_action()
        elif "[Success:" in line:
            self.timer.cancel()
            roll = self.tec.rollPattern.search(line)
            #Successsful action
            if int(roll.group(1)) < int(roll.group(2)):
                self.add_action(Action.unpalm)
            else:
                self.add_action(Action.palm)
        elif "You drop a" in line:
            self.add_action(Action.get_den)


    def palm_timeout(self):
        self.add_action(Action.repeat)
        self.perform_action()

    def perform_action(self):
        if self.free and len(self.queue) > 0:
            self.action = self.queue.pop()
            if self.action == Action.palm:
                self.free = False
                self.send_cmd("p")
                self.timer = Timer(3.0, self.palm_timeout)
                self.timer.start()
            elif self.action == Action.unpalm:
                self.send_cmd("o")
                self.perform_action()
            elif self.action == Action.get_den:
                self.send_cmd("get den")
                self.perform_action()
            elif self.action == Action.repeat:
                self.send_command(self.last_command)


