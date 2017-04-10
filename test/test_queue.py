import unittest
from collections import deque


class CallException(Exception):

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(CallException, self).__init__(message)


class Events(object):
    msg_received = "Message Received"
    msg_proxied = "Message Proxied"
    msg_delivered = "Message Delivered"
    msg_delivery_failed = "Message Delivery Failed"


class Message(object):

    def __init__(self, content):
        self.content = content
        self.failures = 0

    def increment_fail_count(self):
        self.failures = self.failures + 1


class Event(object):

    def __init__(self, source, name, data):
        self.source = source
        self.name = name
        self.data = data

    def __repr__(self):
        return self.name


class Queue(object):

    def __init__(self, name, fail_indexes=None):
        if fail_indexes is None:
            fail_indexes = []

        self.fail_indexes = fail_indexes
        self.name = name
        self.subscribers = []
        self.received_messages = deque([])
        self.consumers = []
        self.rotation = 0

    def publish(self, event):
        for subscriber in self.subscribers:
            subscriber.notify(event)

    def add_subscriber(self, subscriber):
        '''
        Not a subscriber from a workflow perspective this is simply
        the observer pattern.  The Subscribe functionality for the
        worklow is on the Topic.
        '''
        self.subscribers.append(subscriber)

    def add_consumer(self, consumer):
        self.consumers.append(consumer)

    def send(self, msg):
        self.rotation = self.rotation + 1
        if self.rotation - 1 in self.fail_indexes:
            raise CallException('DOWN')
        self.received_messages.append(msg)
        self.publish(Event(self, Events.msg_received, {"msg": msg}))

    def dequeue(self):
        if len(self.consumers) > 0 and len(self.received_messages) > 0:
            consumer = self.consumers[self.rotation % len(self.consumers)]
            msg = self.received_messages.popleft()
            try:
                consumer.process(msg)
                self.publish(Event(self, Events.msg_delivered, {"msg": msg}))
            except CallException:
                msg.increment_fail_count()
                self.received_messages.append(msg)
                self.publish(
                    Event(
                        self, Events.msg_delivery_failed, {
                            "msg": msg}))

    def fail_on_rotation(self, index):
        return Queue(self.name, fail_indexes=self.fail_indexes + [index])

    def continue_failing_for(self, rotations):
        last_index = self.fail_indexes[-1]
        queue_to_return = self
        for index in range(last_index, last_index + rotations):
            queue_to_return = Queue(
                self.name, fail_indexes=queue_to_return.fail_indexes + [index + 1])

        return queue_to_return

    def crank_handle(self):
        self.dequeue()


class TestSubscriber(object):

    def __init__(self):
        self.events = []

    def notify(self, event):
        self.events.append(event)

    def clear(self):
        self.events = []

    def subscribe_to(self, publisher):
        publisher.add_subscriber(self)


class TestWorker(object):

    def __init__(self, fail_indexes=None):
        if fail_indexes is None:
            fail_indexes = []

        self.fail_indexes = fail_indexes
        self.messages = []
        self.counter = 0

    def consume(self, queue):
        queue.add_consumer(self)

    def process(self, message):
        self.counter = self.counter + 1
        if self.counter - 1 in self.fail_indexes:
            raise CallException("FAIL")
        self.messages.append(message)

    def fail_on_message_index(self, index):
        return TestWorker(fail_indexes=self.fail_indexes + [index])


class TestTestWorker(unittest.TestCase):

    def test_fail_on_message_index(self):
        worker = TestWorker().fail_on_message_index(1)

        worker.process(Message("something"))
        with self.assertRaises(CallException):
            worker.process(Message("something"))


class TestQueue(unittest.TestCase):

    def test_queue_publishes_msg_received(self):
        # arrange
        subscriber = TestSubscriber()
        queue = Queue("Q1")
        subscriber.subscribe_to(queue)

        # act
        queue.send(Message("something"))

        # assert
        self.assertEquals(len(subscriber.events), 1)
        self.assertEquals(subscriber.events[0].name, Events.msg_received)

    def test_queue_publishes_msg_delivered(self):
        queue = Queue("Q1")
        queue.send(Message("something"))

        subscriber = TestSubscriber()
        subscriber.subscribe_to(queue)

        worker = TestWorker()
        worker.consume(queue)
        queue.crank_handle()

        self.assertEquals(len(subscriber.events), 1)
        self.assertEquals(subscriber.events[0].name, Events.msg_delivered)

    def test_queue_retries_on_consumer_failure(self):
        queue = Queue("Q1")
        queue.send(Message("something"))

        subscriber = TestSubscriber()
        subscriber.subscribe_to(queue)

        worker = TestWorker().fail_on_message_index(0)
        worker.consume(queue)
        queue.crank_handle()
        queue.crank_handle()

        self.assertEquals(len(subscriber.events), 2)
        self.assertEquals(
            subscriber.events[0].name,
            Events.msg_delivery_failed)
        self.assertEquals(subscriber.events[1].name, Events.msg_delivered)
        self.assertEquals(subscriber.events[1].data["msg"].failures, 1)

    def test_queue_fail_on_rotation(self):
        queue = Queue("Q1").fail_on_rotation(2)
        queue.send(Message("something"))
        queue.send(Message("something"))

        with self.assertRaises(CallException):
            queue.send(Message("something"))

        queue.send(Message("something"))

    def test_queue_fail_on_rotation_for_set_rotations(self):
        queue = Queue("Q1").fail_on_rotation(2).continue_failing_for(2)

        queue.send(Message("something"))
        queue.send(Message("something"))

        with self.assertRaises(CallException):
            queue.send(Message("something"))
        with self.assertRaises(CallException):
            queue.send(Message("something"))
        with self.assertRaises(CallException):
            queue.send(Message("something"))

        queue.send(Message("something"))
