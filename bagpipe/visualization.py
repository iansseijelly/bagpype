"""
Visualization components for rendering pipeline diagrams.

This module contains the matplotlib-based renderer and export functionality.
"""

from dataclasses import dataclass
from typing import Tuple, Optional, List
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path
import seaborn as sns

from bagpipe.models import Node


@dataclass
class RenderConfig:
    figsize: Tuple[float, float] = (12, 8)
    style: str = "whitegrid"
    edge_routing: str = "curved"  # orthogonal or curved
    filename: Optional[str] = None
    font_size: int = 16
    font_family: str = "DejaVu Sans"
    y_label_font_size: int = 12
    x_label_font_size: int = 16


class PipelineRenderer:
    """Renders pipeline diagrams with intelligent edge edge_routing and professional styling."""

    def __init__(self, config: RenderConfig = RenderConfig()):
        """Initialize renderer with a pipeline instance.

        Args:
            pipeline: The Pipeline object to render
        """
        self.parent_pipeline = None  # to be set by the pipeline
        self.config = config
        self.vis_nodes_x: List[int] = []

    def prep_plt(self):
        """Prepare the matplotlib figure and axes."""
        sns.set_style(self.config.style)
        plt.rcParams['font.family'] = self.config.font_family
        plt.rcParams['font.size'] = self.config.font_size

    def get_y_from_node(self, node: Node) -> int:
        """Helper function to get the y-coordinate of a node."""
        return len(self.parent_pipeline.ops) - self.parent_pipeline.get_idx_by_op(node.parent_op)

    def draw_pipeline(self, show: bool = False):
        """Draw the pipeline."""
        fig, ax = plt.subplots(figsize=self.config.figsize)
        total_ops = len(self.parent_pipeline.ops)

        # plot the nodes
        for i, op in enumerate(self.parent_pipeline.ops):
            for k, v in op.nodes.items():
                x = v.time
                y = total_ops - i
                ax.scatter(x, y, marker="s", s=3000, color=v.color,
                           edgecolors="black", alpha=0.6, linewidths=1.5)
                ax.text(x, y, k, ha="center", va="center", fontweight="bold")
                self.vis_nodes_x.append(x)

        # prepare y-ticks
        total_ops = len(self.parent_pipeline.ops)
        y_ticks = [total_ops + 0.5 - i for i in range(total_ops)]
        ax.set_yticks(y_ticks)
        ax.set_ylim(0.5, total_ops + 0.5)
        ax.set_yticklabels([])

        # add y-labels in the middle of the y-ticks
        for i in range(total_ops):
            ax.text(-0.6, y_ticks[i]-0.5, self.parent_pipeline.ops[i].label,
                    ha="right", va="center", fontsize=self.config.y_label_font_size)

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

        # draw edges
        for edge in self.parent_pipeline.edges:
            deps = edge.deps.nodes
            for i in range(len(deps) - 1):
                n1 = deps[i]
                n2 = deps[i + 1]

                sx = n1.time
                sy = self.get_y_from_node(n1)
                tx = n2.time
                ty = self.get_y_from_node(n2)

                # orthogonal edges
                if self.config.edge_routing == "orthogonal":
                    verts = [(sx, sy), (tx, sy), (tx, ty)]
                    codes = [Path.MOVETO, Path.LINETO, Path.LINETO]
                    path = Path(verts, codes)
                    arrow = FancyArrowPatch(
                        path=path,
                        arrowstyle="-|>",
                        color=edge.color,
                        alpha=0.5,
                        lw=2,
                        mutation_scale=14,
                    )
                # curved edges
                elif self.config.edge_routing == "curved":
                    arrow = FancyArrowPatch(
                        (sx, sy),
                        (tx, ty),
                        arrowstyle="-|>",
                        color=edge.color,
                        alpha=0.5,
                        lw=2,
                        mutation_scale=14,
                        connectionstyle="arc3,rad=0.15",
                    )
                else:
                    raise ValueError(f"Invalid edge_routing type: {self.config.edge_routing}")

                ax.add_patch(arrow)

        # add legend
        # collect all edge color-legend pairs for edges with non-empty legends
        edge_color_legend_pairs = {}
        for edge in self.parent_pipeline.edges:
            if edge.has_legend():  # only include edges with non-empty legend
                edge_color_legend_pairs[edge.legend] = edge.color
        # create legend handles and labels
        if edge_color_legend_pairs:
            handles = []
            labels = []
            for legend_text, color in edge_color_legend_pairs.items():
                # create a Line2D object for the legend handle
                from matplotlib.lines import Line2D
                handle = Line2D([0], [0], color=color, lw=2, alpha=0.5)
                handles.append(handle)
                labels.append(legend_text)

            # create and add the legend
            legend = ax.legend(handles, labels, loc='best', fontsize=self.config.y_label_font_size)
            ax.add_artist(legend)

        plt.tight_layout()
        if show:
            plt.show()
        return fig, ax
