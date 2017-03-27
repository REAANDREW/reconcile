
import unittest
from reconcile import control, services

class TestSpike(unittest.TestCase):

    def test_something_works(self):
        simulation = control.Simulation()

        app_service1 = services.ApplicationService(simulation, "AP 1")
        load_balancer1 = services.LoadBalancer(simulation, "LB 1")
        load_balancer1.distribute_to(app_service1)

        message_sender = services.MessageSender()
        message_sender.connect_to(load_balancer1)
        simulation.add_start(message_sender)

        simulation.generate(2)

        self.assertEquals(len(simulation.events), 6)

    def test_something_else_works(self):
        simulation = control.Simulation()

        app_service1 = services.ApplicationService(simulation, "AP 1")
        app_service2 = services.ApplicationService(simulation, "AP 2")
        load_balancer1 = services.LoadBalancer(simulation, "LB 1")

        load_balancer1.distribute_to(app_service1)
        load_balancer1.distribute_to(app_service2)

        message_sender = services.MessageSender()
        message_sender.connect_to(load_balancer1)
        simulation.add_start(message_sender)

        simulation.generate(2)

        print(simulation.events)
        self.assertEquals(len(simulation.events), 6)

    def test_queue(self):
        simulation = control.Simulation()

        app_service1 = services.ApplicationService(simulation, "AP 1")
        app_service2 = services.ApplicationService(simulation, "AP 2")
        load_balancer1 = services.LoadBalancer(simulation, "LB 1")
        load_balancer1.distribute_to(app_service1)
        load_balancer1.distribute_to(app_service2)

        queue1 = services.Queue(simulation, "Q1")
        app_service1.send_to(queue1)
        app_service2.send_to(queue1)

        app_service3 = services.ApplicationService(simulation, "AP 3")
        app_service4 = services.ApplicationService(simulation, "AP 4")
        app_service3.consume_queue(queue1)
        app_service4.consume_queue(queue1)

        message_sender = services.MessageSender()
        message_sender.connect_to(load_balancer1)
        simulation.add_start(message_sender)

        simulation.generate(2)

        print(simulation.events)
        self.assertEquals(len(simulation.events), 14)
