import networkx as nx
from core.stage import get_stage_class

class PipelineExecutor:
    def __init__(self, stages):
        self.stages = {s['name']: s for s in stages}
        self.graph = nx.DiGraph()
        for name, cfg in self.stages.items():
            self.graph.add_node(name)
            for dep in cfg.get('after', []):
                self.graph.add_edge(dep, name)

    def run(self, ctx):
        for name in nx.topological_sort(self.graph):
            stage_cfg = self.stages[name]
            stage_class = get_stage_class(stage_cfg['stage'])
            stage = stage_class()
            ctx.config = stage_cfg.get('config', {})
            stage.setup(ctx)
            stage.process(ctx)
            stage.postprocess(ctx)