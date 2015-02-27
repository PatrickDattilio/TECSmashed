queue = []
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