from reconcile import control
from collections import deque

class Topic:
    pass

class Queue:

    def __init__(self, simulation, name):
        self.simulation = simulation
        self.messages = deque()
        self.name = name
        self.consumers = []
        self.count = 0

    def generate(self):
        self.process()

    def process(self):
        if len(self.messages) > 0 and len(self.consumers) > 0:
            message = self.messages.popleft()
            self.apply(control.Event(self, "message_processed", {"msg": message}))

    def add_consumer(self, consumer):
        self.consumers.append(consumer)

    def send(self, message):
        self.apply(control.Event(self, "message_received", {"msg": message}))

    def apply(self, event):
        method = getattr(self, 'on_'+event.name)
        method(event)
        self.simulation.publish(event)

    def on_message_received(self, evt):
        self.messages.append(evt.data["msg"])

    def on_message_processed(self, evt):
        message = evt.data["msg"]
        consumer = self.consumers[self.count % len(self.consumers)]
        consumer.send(message)
        self.count = self.count + 1


class ApplicationService:

    def __init__(self, simulation, name):
        self.simulation = simulation
        self.name = name
        self.actions = []
        self.destinations = []
        self.messages = deque([])

    #def connect_to(self, node):
    #    node.add(self)

    def consume_queue(self, queue):
        queue.add_consumer(self)

    def generate(self):
        if len(self.messages) > 0 and len(self.destinations) > 0:
            message = self.messages.popleft()
            self.apply(control.Event(self, "message_processed", {"msg": message}))

    def send_to(self, destination):
        self.destinations.append(destination)

    def send(self, message):
        self.apply(control.Event(self, "message_received", {"msg": message}))

    def apply(self, event):
        method = getattr(self, 'on_'+event.name)
        method(event)
        self.simulation.publish(event)

    def send(self, message):
        self.apply(control.Event(self, "message_received", {"msg": message}))

    def on_message_received(self, evt):
        if len(self.destinations) > 0:
            self.messages.append(evt.data["msg"])

    def on_message_processed(self, evt):
        for destination in self.destinations:
            destination.send(evt.data["msg"])

class LoadBalancer:

    def __init__(self, simulation, name):
        self.nodes = []
        self.messages = deque()
        self.simulation = simulation
        self.name = name
        self.count = 0

    def distribute_to(self, node):
        self.nodes.append(node)

    def apply(self, event):
        method = getattr(self, 'on_'+event.name)
        method(event)
        self.simulation.publish(event)

    def send(self, message):
        self.apply(control.Event(self, "message_received", {"msg": message}))

    def forward(self, message):
        self.apply(control.Event(self, "message_proxied", {"msg": message}))

    def on_message_received(self, evt):
        if len(self.nodes) > 0:
            self.messages.append(evt.data["msg"])

    def on_message_proxied(self, evt):
        if len(self.nodes) > 0:
            node = self.nodes[self.count % len(self.nodes)]
            node.send(evt.data["msg"])
            self.count = self.count + 1

    def generate(self):
        if len(self.messages) > 0:
            message = self.messages.popleft()
            self.forward(message)

class MessageSender:

    def __init__(self):
        self.nodes = []

    def connect_to(self, node):
        self.nodes.append(node)

    def generate(self, simulator):
        for node in self.nodes:
            print('message sent')
            node.send("something")
