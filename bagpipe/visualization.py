"""
Visualization components for rendering pipeline diagrams.

This module contains the matplotlib-based renderer and export functionality.
"""

from dataclasses import dataclass
from typing import Tuple, Optional, List
import matplotlib.pyplot as plt
import seaborn as sns
from bagpipe.models import Node


@dataclass
class VisualConfig:
    figsize: Tuple[float, float] = (12, 8)
    style: str = "whitegrid"
    routing: str = "orthogonal"
    filename: Optional[str] = None


class PipelineRenderer:
    """Renders pipeline diagrams with intelligent edge routing and professional styling."""

    def __init__(self, config: VisualConfig = VisualConfig()):
        """Initialize renderer with a pipeline instance.

        Args:
            pipeline: The Pipeline object to render
        """
        self.parent_pipeline = None  # to be set by the pipeline
        self.config = config
        self.vis_nodes_x: List[int] = []
        self.vis_nodes_y: List[int] = []
        self.vis_nodes_list: List[Node] = []
        self.vis_edges: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

    def prep_plt(self):
        """Prepare the matplotlib figure and axes."""
        sns.set_style(self.config.style)
        plt.rcParams['font.family'] = 'DejaVu Sans Mono'
        plt.rcParams['font.size'] = 16

    def draw_pipeline(self):
        """Draw the pipeline."""
        fig, ax = plt.subplots(figsize=self.config.figsize)
        for i, node in enumerate(self.vis_nodes_list):
            ax.scatter(self.vis_nodes_x[i], self.vis_nodes_y[i], marker="s", s=2400, color="white", edgecolors="black")
            ax.text(self.vis_nodes_x[i], self.vis_nodes_y[i], node.label, ha="center", va="center")

        # prepare y-ticks
        total_ops = len(self.parent_pipeline.ops)
        y_ticks = [total_ops + 0.5 - i for i in range(total_ops)]
        ax.set_yticks(y_ticks)
        ax.set_ylim(0.5, total_ops + 0.5)
        ax.set_yticklabels([])

        # add y-labels in the middle of the y-ticks
        # find the longest label
        for i in range(total_ops):
            ax.text(0.3, y_ticks[i]-0.5, f"Op{i} - {self.parent_pipeline.ops[i].label}", ha="right", va="center")

        # prepare x-ticks
        min_time = min(self.vis_nodes_x)
        max_time = max(self.vis_nodes_x)
        x_ticks = [i + 0.5 for i in range(min_time, max_time + 1)]
        ax.set_xticks(x_ticks)
        ax.set_xlim(min_time - 0.5, max_time + 0.5)
        ax.set_xticklabels([])

        # add x-labels in the middle of the x-ticks
        for i in range(min_time, max_time + 1):
            ax.text(i, 0.4, f"{i}", ha="center", va="center")

        plt.tight_layout()
        plt.show()
