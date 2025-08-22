"""
Core model classes for the Bagpype library.

This module contains the main classes that users interact with:
Op, Node, and NodeList.
"""

from typing import List


class NodeStyle:
    def __init__(self, color: str = "white", linestyle: str = "-"):
        self.color = color
        self.linestyle = linestyle


class Node:
    def __init__(self, label: str, time: int, style: NodeStyle = NodeStyle()):
        self.label = label
        self.time = time
        self.style = style
        # parent op is set and maintained by the Op class

    def __repr__(self):
        return f"{self.label}@{self.time}"

    def __rshift__(self, other):
        """Support for '>>' syntax: node1 >> node2 creates a chain"""
        if isinstance(other, NodeList):
            edge = NodeList([self] + other.nodes)
        elif isinstance(other, Node):
            edge = NodeList([self, other])
        else:
            raise TypeError(f"Connecting nodes with invalid type: {type(other)}")

        return edge

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.label == other.label and
                self.time == other.time and
                self.parent_op == other.parent_op)


class Op:
    def __init__(self, label):
        self.label = label
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
        node.parent_op = self
        return node

    def add_node(self, node: Node):
        self.nodes[node.label] = node
        node.parent_op = self
        return self


class NodeList:
    # a linked list of nodes
    def __init__(self, nodes):
        self.nodes = nodes

    def __rshift__(self, other):
        """Support for '>>' syntax: node1 >> node2 creates an nodelist"""
        if isinstance(other, NodeList):
            edge = NodeList(self.nodes + other.nodes)
        elif isinstance(other, Node):
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


class EdgeStyle:
    def __init__(self, color: str = "black", linestyle: str = "-"):
        self.color = color
        self.linestyle = linestyle


class Edge:
    def __init__(self, deps: NodeList | List[Node], style: EdgeStyle = EdgeStyle(), legend: str = ""):
        self.deps = deps if isinstance(deps, NodeList) else NodeList(deps)
        self.style = style
        self.legend = legend

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return (self.deps == other.deps and
                self.style == other.style and
                self.legend == other.legend)

    def __repr__(self):
        return f"Edge(deps={self.deps}, style={self.style}, " \
               f"legend={self.legend})"

    # return self for chaining setters
    def set_edge_color(self, color: str):
        self.style.color = color
        return self

    def set_edge_legend(self, legend: str):
        self.legend = legend
        return self

    def set_node_color(self, color: str, overwrite: bool = False):
        for node in self.deps.nodes:
            if overwrite:
                node.style.color = color
            else:
                node.style.color = color if node.style.color == "white" else node.style.color
        return self

    def has_legend(self):
        return self.legend != ""
