import networkx as nx
from core.registry import registry
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
import copy

class PipelineExecutor:
    def __init__(self, stages):
        self.stages = {s['name']: s for s in stages}
        self.graph = nx.DiGraph()
        for name, cfg in self.stages.items():
            self.graph.add_node(name)
            after = cfg.get("after", [])
            if isinstance(after, str):
                after = [after]
            for dep in after:
                self.graph.add_edge(dep, name)

    def run(self, ctx):
        for name in nx.topological_sort(self.graph):
            stage_cfg = self.stages[name]
            stage_class = registry.get_stage_class(stage_cfg['stage'])
            stage = stage_class()
            ctx.config = stage_cfg.get('config', {})
            stage.setup(ctx)
            stage.process(ctx)
            stage.postprocess(ctx)