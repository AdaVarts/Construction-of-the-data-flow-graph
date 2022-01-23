import typing
from node import Node
from edge import Edge


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

    # removes all edges that represent 'key' - store -> 'key.1'
    # only variables such as 'key' is left in tree
    def rearange(self):
        edges_IDs = []
        possible_repeats = []
        for edge in self.edges:
            if edge.name == "store" and '-' in edge.tail.name:
                node_t_name = edge.tail.name.split('-')[1]
                node_h_name = edge.head.name.split('-')[1]
                if node_h_name.split('.')[0] == '': continue
                if node_t_name == node_h_name.split('.')[0] and node_h_name.split('.')[1] == '1':
                    possible_repeats.append(node_h_name)
                    edges_IDs.append(self.edges.index(edge))
        for edge in self.edges:
            for n in possible_repeats:
                if len(edge.tail.name.split('-'))>1 and edge.tail.name.split('-')[1] == n:
                    edge.tail.name = edge.tail.name.split('.')[0]
                if len(edge.head.name.split('-'))>1 and edge.head.name.split('-')[1] == n:
                    edge.head.name = edge.head.name.split('.')[0]
        edges_IDs.reverse()
        for e_i in edges_IDs:
            self.edges.remove(self.edges[e_i])

    def __str__(self) -> str:
        str = ""
        for edge in self.edges:
            str+=edge.name+":  \n"
            if edge.tail is not None:
                str+="tail- "+edge.tail.name+"\n"
            if edge.head is not None:
                str+="head- "+edge.head.name+"\n"
        return str
