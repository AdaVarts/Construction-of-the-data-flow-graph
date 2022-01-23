from node import Node
class Edge:
    def __init__(self, name, tail: Node = None, head: Node = None):
        self.name = name
        self.tail = tail
        self.head = head
        if tail is not None: self.tail.outgoing.append(self)
        if head is not None: self.head.incoming.append(self)
    
    def __str__(self) -> str:
        return self.name