"""
Top-level pipeline classes for the Bagpipe library.

This module collects user-level specification from models.py
and combines with the visualization-level specification from visualization.py
"""

from typing import List
from .models import Op, Edge
from .visualization import PipelineRenderer


class Pipeline:
    def __init__(self):
        self.ops: List[Op] = []
        self.edges: List[Edge] = []
        self.renderer = PipelineRenderer()
        self.renderer.parent_pipeline = self

    def __add__(self, other):
        if isinstance(other, Op):
            self.add_op(other)
        elif isinstance(other, Edge):
            self.add_edge(other)
        else:
            raise TypeError(f"Adding invalid type: {type(other)}")
        return self

    def add_op(self, op: Op):
        self.ops.append(op)
        return self

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        return self

    def draw(self):
        self.renderer.prep_plt()
        self.renderer.draw_pipeline()
