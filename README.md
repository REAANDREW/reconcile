# IDEAS

## Connections

Think about which direction the connection will be going in to assertain which node should be connecting to which node e.g.

A load balancer will connect to application services so they can distribute the load to them so:

```python
loadBalancer = LoadBalancer()
appService = ApplicationService()
loadBalancer.connect_to(app_service)
```

If this is how the connections are made then it is the connecting service who has the responsibility of ascertaining whether or not the node it is connecting to is acceptable or in other words, has the correct interface.

For this example it is quite simple as a load balancer can be connected to any node but; what happens when the connection is made?

```python
def connect_to(self, other_node):
    self.add_to_pool(other_node)
```

If this was the other way around i.e. the ApplicationService was connecting to the LoadBalancer (so it could send traffic) it would be implemented something like this:

```python
def connect_to(self, other_node):
    self.add_upstream_service(other_node)
```

### Connecting in the GUI

When dragging a connection line between two nodes, the label of the line should be derived from the type of the node ar source to the type of the node at destination e.g.

**Drag from Queue to Application Service**

```shell
Q1<------consumes------AS1
```

**Drag from Application Service to Queue**

```shell
AS1-------sends_to----->Q1
```
