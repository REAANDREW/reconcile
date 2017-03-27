from collections import deque

class Event:

    def __init__(self, sender, name, data={}):
        self.sender = sender
        self.name = name
        self.data = data

    def __repr__(self):
        return self.name

class GenerationEvent:

    def __init__(self, event, generation):
        self.event = event
        self.generation = generation

    def __repr__(self):
        return '{instance}:{name}:G[{generation}]'.format(name = self.event.name, generation = self.generation, instance=self.event.sender.name)

class Simulation:

    def __init__(self):
        self.worker_nodes = []
        self.starter_nodes = []
        self.events = []
        self.next_gen = deque([])
        self.generation = 0

    def add_start(self, node):
        self.starter_nodes.append(node)

    def generate(self, number):
        next_nodes = deque(self.next_gen)
        
        for i in range(0, number):
            self.generation = self.generation + 1

            while len(next_nodes) > 0:
                node = next_nodes.popleft()
                node.generate(self)
            
            self.next_gen=deque([])

            for node in self.starter_nodes:
                node.generate(self)

    def publish(self, event):
        sender = event.sender
        self.events.append(GenerationEvent(event, self.generation))

        if sender not in self.next_gen:
            self.next_gen.append(sender)
            sender.generate()  
