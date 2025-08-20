"""
Bagpipe - A Python DSL for processor pipeline visualization.

This package provides a domain-specific language for describing and visualizing
processor pipeline diagrams using matplotlib.
"""

__version__ = "0.1.0"

# Import main classes for easy access
# TODO: Uncomment when models are implemented
from .models import Pipeline, Op, Node, Edge, Chain

__all__ = [
    "Pipeline",
    "Op",
    "Node",
    "Edge",
    "Chain",
]
