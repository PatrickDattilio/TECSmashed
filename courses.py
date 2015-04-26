from threading import Timer
from Action import Action


class courses:
    def __init__(self, tec):
        self.tec = tec
        self.timer = Timer(2.0, self.timeout)

    def timeout(self):
        print("Timeout: "+str(self.tec.action))
        self.tec.add_action(Action.repeat)
        self.tec.free = True
        self.tec.perform_action()

    def go(self):
        self.tec.free = True
        self.perform_action()

    def perform_action(self):
        if self.tec.free and len(self.tec.queue) > 0:
            self.tec.action = self.tec.queue.pop()
            if self.tec.action == Action.stand:
                self.tec.send_cmd("stand")
            elif self.tec.action == Action.east:
                self.tec.send_cmd("e")
            elif self.tec.action == Action.south:
                self.tec.send_cmd("s")
            elif self.tec.action == Action.climb_rope:
                self.tec.send_cmd("cc", 250)
                self.timer = Timer(4.0, self.timeout)
                self.timer.start()
            elif self.tec.action == Action.go_plank:
                self.tec.send_cmd("cv")
                self.timer = Timer(4.0, self.timeout)
                self.timer.start()
            elif self.tec.action == Action.go_path:
                self.tec.send_cmd("cb")
                self.timer = Timer(3.0, self.timeout)
                self.timer.start()
            elif self.tec.action == Action.jump_rope:
                self.tec.send_cmd("cg", 350)
            elif self.tec.action == Action.go_track:
                self.tec.send_cmd("ch", 350)
            elif self.tec.action == Action.go_coals:
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

        elif "You start to climb up the rope." in line or "You pick a plank and begin to walk over the water." in line or "You run down the path as fast as you can!" in line:
            self.timer.cancel()
