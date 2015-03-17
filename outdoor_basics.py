from Action import Action

class outdoor_basics:
    def __init__(self, tec):
        self.tec = tec

    def perform_action(self):
        if self.tec.free and len(self.tec.queue) > 0:
            self.action = self.tec.queue.pop()
            print("OAction: "+ str(self.action))
            if self.action == Action.find_firewood:
                self.tec.add_action(Action.find_firewood)
                self.handle_find_firewood()
            elif self.action == Action.make_torch:
                self.tec.add_action(Action.make_torch)
                self.handle_make_torch()
            else:
                self.tec.perform_action()

    # We are in combat
    def handle_outdoor_line(self, line):
        if "You are no longer busy." in line:
            print("Not Busy")
            self.tec.free = True
            self.perform_action()
        elif "ff" in line:
            self.tec.add_action(Action.find_firewood)
        elif "mt" in line:
            self.tec.add_action(Action.make_torch)

    def handle_find_firewood(self):
        self.tec.send_cmd("ff")

    def handle_make_torch(self):
        self.tec.send_cmd("mt")
