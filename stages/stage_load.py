from core.stage import Stage, register_stage
import pandas as pd

@register_stage("LoadData")
class LoadData(Stage):
    def setup(self, ctx):
        pass

    def process(self, ctx):
        ctx.metadata["data"] = pd.read_csv(ctx.config["path"])

    def postprocess(self, ctx):
        pass
