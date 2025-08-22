"""
Bagpype - A Python library for processor pipeline visualization.

This package provides a domain-specific language for describing and visualizing
processor pipeline diagrams using matplotlib.
"""

__version__ = "0.1.0"

# Import main classes for easy access
from .models import Op, Node, Edge, NodeList, NodeStyle, EdgeStyle
from .pipeline import Pipeline

__all__ = [
    "Pipeline",
    "Op",
    "Node",
    "Edge",
    "NodeList",
    "NodeStyle",
    "EdgeStyle",
]
