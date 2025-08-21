"""
Visualization components for rendering pipeline diagrams.

This module contains the matplotlib-based renderer and export functionality.
"""

from dataclasses import dataclass
from typing import Tuple, Optional, List
import matplotlib.pyplot as plt
import seaborn as sns


@dataclass
class VisualConfig:
    figsize: Tuple[float, float] = (12, 8)
    style: str = "whitegrid"
    routing: str = "orthogonal"
    filename: Optional[str] = None
    font_size: int = 16
    font_family: str = "DejaVu Sans Mono"
    y_label_font_size: int = 12
    x_label_font_size: int = 16


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

    def prep_plt(self):
        """Prepare the matplotlib figure and axes."""
        sns.set_style(self.config.style)
        plt.rcParams['font.family'] = self.config.font_family
        plt.rcParams['font.size'] = self.config.font_size

    def draw_pipeline(self):
        """Draw the pipeline."""
        fig, ax = plt.subplots(figsize=self.config.figsize)
        total_ops = len(self.parent_pipeline.ops)
        for i, op in enumerate(self.parent_pipeline.ops):
            for k, v in op.nodes.items():
                x = v.time
                y = total_ops - i
                ax.scatter(x, y, marker="s", s=2400, color="white", edgecolors="black")
                ax.text(x, y, k, ha="center", va="center")
                self.vis_nodes_x.append(x)

        # prepare y-ticks
        total_ops = len(self.parent_pipeline.ops)
        y_ticks = [total_ops + 0.5 - i for i in range(total_ops)]
        ax.set_yticks(y_ticks)
        ax.set_ylim(0.5, total_ops + 0.5)
        ax.set_yticklabels([])

        # add y-labels in the middle of the y-ticks
        for i in range(total_ops):
            ax.text(0.4, y_ticks[i]-0.5, f"Op{i} - {self.parent_pipeline.ops[i].label}",
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

        plt.tight_layout()
        plt.show()
