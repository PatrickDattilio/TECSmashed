from Action import Action

snare_phrases = ["but nothing is trapped inside", "rendering it useless", "is trapped inside", "fallen in"]

class hunting_lore:
    def __init__(self, tec):
        self.tec = tec

    def perform_action(self):
        if self.tec.free and len(self.tec.queue) > 0:
            self.action = self.tec.queue.pop()
            print("OAction: "+ str(self.action))
            # if self.action == Action.find_firewood: