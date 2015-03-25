from threading import Timer

from Action import Action


class pickpocketing:
    global running

    def __init__(self, tec):
        self.tec = tec
        self.free = False
        self.queue = []
        self.action = Action.nothing
        self.timer = Timer(3.0, self.perform_action())
        self.last_command = ""
        self.palming = False

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
        self.send_cmd(self.last_command)


    def handle_pickpocket_line(self, line):
        if line.strip() == "You are no longer busy.":
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
        elif "You drop" in line:
            self.add_action(Action.get_den)
            self.add_action(Action.palm)

    def perform_action(self):
        if self.free and len(self.queue) > 0:
            self.action = self.queue.pop()
            if self.action == Action.palm:
                self.free = False
                self.send_cmd("p")
                self.timer = Timer(5.0, self.palm_timeout)
                self.timer.start()
            elif self.action == Action.unpalm:
                self.send_cmd("o")
                self.perform_action()
                self.timer = Timer(5.0, self.palm_timeout)
                self.timer.start()
            elif self.action == Action.get_den:
                self.send_cmd("get den")
                self.perform_action()
            elif self.action == Action.spook:
                self.add_action(Action.spook)
                self.send_cmd("spookt")
            elif self.action == Action.ear:
                self.add_action(Action.ear)
                self.send_cmd("ect")
            elif self.action == Action.repeat:
                self.retry()


