from Action import Action


class courses:
    def __init__(self, tec):
        self.tec = tec

    def perform_action(self):
        if self.tec.free and len(self.tec.queue) > 0:
            self.action = self.tec.queue.pop()
            if self.action == Action.stand:
                self.tec.send_cmd("stand")
            elif self.action == Action.east:
                self.tec.send_cmd("e")
            elif self.action == Action.south:
                self.tec.send_cmd("s")
            elif self.action == Action.climb_rope:
                self.tec.send_cmd("cc", 250)
            elif self.action == Action.go_plank:
                self.tec.send_cmd("cv")
            elif self.action == Action.go_path:
                self.tec.send_cmd("cb")
            elif self.action == Action.jump_rope:
                self.tec.send_cmd("cg", 350)
            elif self.action == Action.go_track:
                self.tec.send_cmd("ch", 350)
            elif self.action == Action.go_coals:
                self.tec.send_cmd("cj", 350)


    def handle_courses_line(self, line):
        if "You are no longer busy." in line:
            print("Not Busy")
            self.go()
        elif "Several trainers drag you back to the start." in line:
            self.tec.add_action(Action.stand)
            if self.tec.courses_part_three:
                self.tec.add_action(Action.east)
            else:
                self.tec.add_action(Action.south)
            self.go()
        elif "You arrive at a climbing wall." in line:
            self.tec.add_action(Action.climb_rope)
            self.go()
        elif "You arrive at a pool." in line:
            self.tec.add_action(Action.go_plank)
            self.go()
        elif "You arrive at a dropping pole." in line or "You arrive at a path through swinging weights." in line:
            self.tec.add_action(Action.go_path)
            self.go()
        elif "You slowly jog towards the start" in line:
            self.tec.add_action(Action.east)
            self.go()
        elif "You arrive at a mud pit." in line:
            self.tec.add_action(Action.jump_rope)
            self.go()
        elif "You arrive at a circular track." in line:
            self.tec.add_action(Action.go_track)
            self.go()
        elif "You arrive at a bed of hot coals" in line:
            self.tec.add_action(Action.go_coals)
            self.go()
        elif "You feel as if you have improved" in line:
            if self.tec.courses_part_three:
                self.tec.add_action(Action.east)
            else:
                self.tec.add_action(Action.south)
            self.go()

            # elif "You start to climb up the rope." in line:

    def go(self):
        self.tec.free = True
        self.perform_action()