import typing

class Function:
    def __init__(self, name, params):
        self.name = name
        self.params = params
        self.labels = []
        self.label_map = {}
        self.ssa_map_lbl = {}
        self.ssa_map_var = {}
    
    def init_ssamap(self, source_labels):
        for l in source_labels:
            self.ssa_map_lbl[l.name] = 0
    
    def init_ssavarmap(self, source_labels):
        for l in source_labels:
            for op in l.operations:
                if op.name != 'br' and op.name != 'ret' and op.value != '' \
                   and op.value not in self.ssa_map_var.keys():
                    self.ssa_map_var[op.value] = 0
    
class Operation:
    def __init__(self, name, value=None, args=None):
        self.name = name
        self.value = value
        self.args = args

class Label:
    def __init__(self, name):
        self.name = name
        self.operations = []

# DFG structure
class Node:
    def __init__(self, name):
        self.name = name
        self.incoming = []
        self.outgoing = []

    def __str__(self) -> str:
        return self.name

class Edge:
    def __init__(self, name, tail: Node = None, head: Node = None):
        self.name = name
        self.tail = tail
        self.head = head
        if tail is not None: self.tail.outgoing.append(self)
        if head is not None: self.head.incoming.append(self)
    
    def __str__(self) -> str:
        return self.name

# node: name - variable+func.name; incom, outcom ::edge   +   edge:name - instr; tail, head ::node
class DFG:
    def __init__(self):
        self.edges: typing.List(Edge) = []
        self.nodes: typing.Dict(str, Node) = {}

    def get_node(self, node_name):
        if node_name in self.nodes:
            return self.nodes[node_name]
        else:
            return None

    def __str__(self) -> str:
        str = ""
        for edge in self.edges:
            str+=edge.name+":  \n"
            if edge.tail is not None:
                str+="tail- "+edge.tail.name+"\n"
            if edge.head is not None:
                str+="head- "+edge.head.name+"\n"
        return str