"""
Top-level pipeline classes for the Bagpype library.

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

    def draw(self, save: bool = False, filename: str = "pipeline.png"):
        self.renderer.prep_plt()
        show = not save
        fig, ax = self.renderer.draw_pipeline(show)
        if save:
            fig.savefig(filename)
        return fig, ax

    def get_idx_by_op(self, op: Op) -> int:
        return self.ops.index(op)

    def get_op_by_idx(self, idx: int) -> Op:
        return self.ops[idx]
