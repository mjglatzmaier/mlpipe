"""DAG-based pipeline executor with topological stage ordering."""

from __future__ import annotations

from typing import Any

import networkx as nx

from .registry import registry


class PipelineExecutor:
    """Build and run a directed acyclic graph of pipeline stages.

    Parameters:
        stages: A list of stage descriptors, each a dict with at least
            ``name`` (unique id) and ``stage`` (registered class name).
            Optional keys: ``after`` (dependency name or list of names)
            and ``config`` (dict passed to the stage at runtime).

    Example::

        stages = [
            {"name": "load",  "stage": "DataLoader", "config": {"path": "data.csv"}},
            {"name": "train", "stage": "Trainer",    "after": "load"},
        ]
        executor = PipelineExecutor(stages)
        executor.run(ctx)
    """

    def __init__(self, stages: list[dict[str, Any]]) -> None:
        self.stages: dict[str, dict[str, Any]] = {s["name"]: s for s in stages}
        self.graph = nx.DiGraph()

        for name, cfg in self.stages.items():
            self.graph.add_node(name)
            after = cfg.get("after", [])
            if isinstance(after, str):
                after = [after]
            for dep in after:
                if dep not in self.stages:
                    raise ValueError(
                        f"Stage '{name}' depends on '{dep}', "
                        f"which is not defined in the pipeline."
                    )
                self.graph.add_edge(dep, name)

        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Pipeline contains a cycle — stages must form a DAG.")

    def run(self, ctx) -> None:
        """Execute all stages in topological order.

        Each stage receives its own ``config`` dict via
        ``ctx.stage_config`` (the global ``ctx.config`` is not modified).
        """
        for name in nx.topological_sort(self.graph):
            stage_cfg = self.stages[name]
            stage_class = registry.get_stage_class(stage_cfg["stage"])
            stage = stage_class()

            # Expose per-stage config without clobbering the global config.
            ctx.stage_config = stage_cfg.get("config", {})

            stage.setup(ctx)
            stage.process(ctx)
            stage.postprocess(ctx)
