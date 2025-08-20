"""
Core model classes for the Bagpipe library.

This module contains the main classes that users interact with:
Pipeline, Op, Node, and Chain.
"""

from typing import List


class Pipeline:
    def __init__(self):
        self.instructions = []
        self.edges = []

    def __add__(self, other):
        if isinstance(other, Op):
            self.instructions.append(other)
        elif isinstance(other, Edge):
            self.edges.append(other)
        else:
            raise TypeError(f"Adding invalid type: {type(other)}")
        return self

    def add_op(self, op: Op):
        self.instructions.append(op)
        return self

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        return self

    def draw(self):
        pass


class Node:
    def __init__(self, label: str, cycle: int, color: str = "white"):
        self.label = label
        self.cycle = cycle
        self.color = color

    def __repr__(self):
        return f"{self.label}@{self.cycle}"

    def __rshift__(self, other):
        """Support for '->' syntax: node1 >> node2 creates an edge"""
        if isinstance(other, Chain):
            print(f"chaining node {self} with edge {other}")
            edge = Chain([self] + other.nodes)
        elif isinstance(other, Node):
            print(f"chaining node {self} with node {other}")
            edge = Chain([self, other])
        else:
            raise TypeError(f"Chaining nodes with invalid type: {type(other)}")

        return edge

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.label == other.label and
                self.cycle == other.cycle and
                self.color == other.color)


class Op:
    def __init__(self, name):
        self.name = name
        self.nodes = {}

    def __getattr__(self, label):
        # If the node already exists, return it
        if label in self.nodes:
            return self.nodes[label]
        else:
            # If the node doesn't exist, create it
            # We need to return a callable that can create the node with arguments
            def create_node(*args):
                if len(args) != 1:
                    raise ValueError(f"Node creation requires exactly one argument (cycle), got {len(args)}")
                node = Node(label, args[0])
                self.nodes[label] = node
                return node
            return create_node

    def add_node(self, node: Node):
        self.nodes[node.label] = node
        return self


class Chain:
    # a linked list of nodes
    def __init__(self, nodes):
        self.nodes = nodes

    def __rshift__(self, other):
        """Support for '->' syntax: node1 >> node2 creates an edge"""
        if isinstance(other, Chain):
            print(f"chaining edge {self} with edge {other}")
            edge = Chain(self.nodes + other.nodes)
        elif isinstance(other, Node):
            print(f"chaining edge {self} with node {other}")
            edge = Chain(self.nodes + [other])
        else:
            raise TypeError(f"Chaining edges with invalid type: {type(other)}")

        return edge

    def __eq__(self, other):
        if not isinstance(other, Chain):
            return False
        return self.nodes == other.nodes

    def __repr__(self):
        return " >> ".join(map(str, self.nodes))


class Edge:
    def __init__(self, deps: Chain | List[Node], color: str, legend: str = ""):
        self.deps = deps if isinstance(deps, Chain) else Chain(deps)
        self.color = color
        self.legend = legend

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return (self.deps == other.deps and
                self.color == other.color and
                self.legend == other.legend)

    def __repr__(self):
        return f"Edge(deps={self.deps}, color={self.color}, legend={self.legend})"
