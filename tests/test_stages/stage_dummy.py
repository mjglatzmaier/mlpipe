"""Example dummy stage for testing."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mlpipe.core.registry import registry
from mlpipe.core.stage import Stage
from mlpipe.utils.mode import PipelineMode

if TYPE_CHECKING:
    from mlpipe.core.context import PipelineContext


@registry.register_stage("DummyStage")
class DummyStage(Stage):
    """A no-op stage used in tests and examples."""

    def setup(self, ctx: PipelineContext) -> None:
        ctx.metadata["setup"] = True

    def process(self, ctx: PipelineContext) -> None:
        ctx.metadata["process"] = True

        if ctx.mode == PipelineMode.TRAIN:
            self._process_train(ctx)
        elif ctx.mode == PipelineMode.INFER:
            self._process_infer(ctx)
        elif ctx.mode == PipelineMode.LABEL:
            self._process_label(ctx)
        else:
            raise ValueError(f"Unsupported mode: {ctx.mode}")

    def postprocess(self, ctx: PipelineContext) -> None:
        ctx.metadata["postprocess"] = True

    def _process_train(self, ctx: PipelineContext) -> None:
        pass

    def _process_infer(self, ctx: PipelineContext) -> None:
        message = ctx.stage_config.get("message", "no message provided")
        ctx.metadata["infer_message"] = message
        if "sleep" in ctx.stage_config:
            import time
            time.sleep(ctx.stage_config["sleep"])
