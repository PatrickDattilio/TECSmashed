from Action import Action

class outdoor_basics:
    def __init__(self, tec):
        self.tec = tec

    def perform_action(self):
        if self.tec.free and len(self.tec.queue) > 0:
            self.tec.action = self.tec.queue.pop()
            print("OAction: "+ str(self.tec.action))
            if self.tec.action == Action.find_firewood:
                self.tec.add_action(Action.find_firewood)
                self.handle_find_firewood()
            elif self.tec.action == Action.make_torch:
                self.tec.add_action(Action.make_torch)
                self.handle_make_torch()
            elif self.tec.action == Action.stoke_fire_twig:
                self.tec.add_action(Action.stoke_fire_twig)
                self.handle_stoke_fire_twig()
            elif self.tec.action == Action.find_grass:
                self.tec.add_action(Action.find_grass)
                self.handle_find_grass()
            elif self.tec.action == Action.find_berries:
                self.tec.add_action(Action.find_berries)
                self.handle_find_berries()
            elif self.tec.action == Action.find_twig:
                self.tec.add_action(Action.find_twig)
                self.handle_find_twig()
            elif self.tec.action == Action.make_rope:
                self.tec.add_action(Action.make_rope)
                self.handle_make_rope()
            else:
                self.tec.perform_action()

    def handle_outdoor_line(self, line):

        if "ff" in line:
            self.tec.add_action(Action.find_firewood)
        elif "You don't see any \"branch\" here." in line:
            self.tec.remove_action(Action.make_torch)
        elif "mt" in line:
            self.tec.add_action(Action.make_torch)
        elif "sft" in line:
            self.tec.add_action(Action.stoke_fire_twig)
        elif "fg" in line:
            self.tec.add_action(Action.find_grass)
        elif "fb" in line:
            self.tec.add_action(Action.find_berries)
        elif "gt" in line:
            self.tec.add_action(Action.find_twig)
        elif "mr" in line:
            self.tec.add_action(Action.make_rope)
        if "You are no longer busy." in line:
            print("Not Busy")
            self.tec.free = True
            self.perform_action()

    def handle_find_firewood(self):
        self.tec.send_cmd("ff")

    def handle_make_torch(self):
        self.tec.send_cmd("mt")

    def handle_stoke_fire_twig(self):
        self.tec.send_cmd("sft")

    def handle_find_berries(self):
        self.tec.send_cmd("fb")

    def handle_find_grass(self):
        self.tec.send_cmd("fg")

    def handle_find_twig(self):
        self.tec.send_cmd("gt")

    def handle_make_rope(self):
        self.tec.send_cmd("mr")
