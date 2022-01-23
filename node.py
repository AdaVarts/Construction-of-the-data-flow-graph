
class Node:
    def __init__(self, name):
        self.name = name
        self.incoming = []
        self.outgoing = []

    def __str__(self) -> str:
        return self.name