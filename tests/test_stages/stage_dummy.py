from core.stage import Stage, register_stage
from core.context import PipelineContext

@register_stage("DummyStage")
class DummyStage(Stage):
    def setup(self, ctx):
        ctx.metadata["setup"] = True

    def process(self, ctx):
        message = ctx.config.get("message", "no message provided")
        print(f"[Dummy] Processing with message: {message}")
        ctx.metadata["process"] = True
        if "sleep" in ctx.config:
            import time
            time.sleep(ctx.config["sleep"])

    def postprocess(self, ctx):
        ctx.metadata["postprocess"] = True