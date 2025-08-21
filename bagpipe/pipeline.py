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

    def prep_vis_data(self):
        """
        Prepare the data needed for visualization.
        Convert user models to visualization coordinates, and store them in the renderer.
        """
        vis_nodes_x = []
        vis_nodes_y = []
        vis_nodes_list = []
        vis_edges = []

        total_ops = len(self.ops)
        for i, op in enumerate(self.ops):
            for k, v in op.nodes.items():
                vis_nodes_x.append(v.time)
                vis_nodes_y.append(total_ops - i)
                vis_nodes_list.append(v)
        for edge in self.edges:
            vis_edges.append(edge)

        self.renderer.vis_nodes_x = vis_nodes_x
        self.renderer.vis_nodes_y = vis_nodes_y
        self.renderer.vis_nodes_list = vis_nodes_list
        self.renderer.vis_edges = vis_edges

    def draw(self):
        self.renderer.prep_plt()
        self.prep_vis_data()
        self.renderer.draw_pipeline()
