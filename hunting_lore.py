from Action import Action

snare_phrases = ["but nothing is trapped inside", "rendering it useless", "is trapped inside", "fallen in"]

class hunting_lore:
    def __init__(self, tec):
        self.tec = tec

    def perform_action(self):
        if self.tec.free and len(self.tec.queue) > 0:
            self.tec,action = self.tec.queue.pop()
            print("Hunting: "+ str(self.tec.action))
            # if self.tec.action == Action.find_firewood:

    def handle_hunting_line(self, line):
        if snare_phrases[0] in line:
            self.move()
        elif snare_phrases[1] in line:
            self.dismantle()
        elif snare_phrases[2] in line or snare_phrases[3] in line:
            self.release()

    def move(self):
        pass

    def dismantle(self):
        pass

    def release(self):
        pass