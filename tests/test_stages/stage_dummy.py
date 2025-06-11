from core.stage import Stage, register_stage
from core.context import PipelineContext
from utils.mode import PipelineMode

@register_stage("DummyStage")
class DummyStage(Stage):
    def setup(self, ctx):
        ctx.metadata["setup"] = True

    def process(self, ctx):
        if ctx.mode == PipelineMode.TRAIN:
            self.process_train(ctx)
        elif ctx.mode == PipelineMode.LABEL:
            self.process_label(ctx)
        elif ctx.mode == PipelineMode.INFER:
            self.process_infer(ctx)
        else:
            raise ValueError(f"Unsupported mode: {ctx.mode}")

    def postprocess(self, ctx):
        ctx.metadata["postprocess"] = True

    def process_train(self, ctx):
        print("Processing in TRAIN mode.")

    def process_label(self, ctx):
        print("Processing in LABEL mode.")

    def process_infer(self, ctx):
        message = ctx.config.get("message", "no message provided")
        print(f"[Dummy] Processing with message: {message}")
        ctx.metadata["process"] = True
        if "sleep" in ctx.config:
            import time
            time.sleep(ctx.config["sleep"])