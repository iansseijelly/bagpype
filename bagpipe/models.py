"""
Core model classes for the Bagpipe library.

This module contains the main classes that users interact with:
Op, Node, and NodeList.
"""

from typing import List


class Node:
    def __init__(self, label: str, cycle: int, color: str = "white"):
        self.label = label
        self.cycle = cycle
        self.color = color

    def __repr__(self):
        return f"{self.label}@{self.cycle}"

    def __rshift__(self, other):
        """Support for '>>' syntax: node1 >> node2 creates a chain"""
        if isinstance(other, NodeList):
            print(f"chaining node {self} with edge {other}")
            edge = NodeList([self] + other.nodes)
        elif isinstance(other, Node):
            print(f"chaining node {self} with node {other}")
            edge = NodeList([self, other])
        else:
            raise TypeError(f"Connecting nodes with invalid type: {type(other)}")

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
        if label in self.nodes:
            return self.nodes[label]
        else:
            return lambda *args: self.create_node(label, *args)

    def create_node(self, label, *args):
        if label in self.nodes:
            raise ValueError(f"Node {label} already exists")
        node = Node(label, *args)
        self.nodes[label] = node
        return node

    def add_node(self, node: Node):
        self.nodes[node.label] = node
        return self


class NodeList:
    # a linked list of nodes
    def __init__(self, nodes):
        self.nodes = nodes

    def __rshift__(self, other):
        """Support for '->' syntax: node1 >> node2 creates an edge"""
        if isinstance(other, NodeList):
            print(f"chaining edge {self} with edge {other}")
            edge = NodeList(self.nodes + other.nodes)
        elif isinstance(other, Node):
            print(f"chaining edge {self} with node {other}")
            edge = NodeList(self.nodes + [other])
        else:
            raise TypeError(f"NodeListing edges with invalid type: {type(other)}")

        return edge

    def __eq__(self, other):
        if not isinstance(other, NodeList):
            return False
        return self.nodes == other.nodes

    def __repr__(self):
        return " >> ".join(map(str, self.nodes))


class Edge:
    def __init__(self, deps: NodeList | List[Node], color: str = "black", legend: str = ""):
        self.deps = deps if isinstance(deps, NodeList) else NodeList(deps)
        self.color = color
        self.legend = legend

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return (self.deps == other.deps and
                self.color == other.color and
                self.legend == other.legend)

    def __repr__(self):
        return f"Edge(deps={self.deps}, color={self.color}, " \
               f"legend={self.legend})"

    def set_color(self, color: str):
        self.color = color
        return self

    def set_legend(self, legend: str):
        self.legend = legend
        return self
