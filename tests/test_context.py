"""Tests for the PipelineContext."""

from mlpipe.core.context import PipelineContext
from mlpipe.utils.mode import DebugLevel, PipelineMode


class TestPipelineContext:
    def test_defaults(self):
        ctx = PipelineContext()
        assert ctx.debug == DebugLevel.DEBUG
        assert ctx.mode == PipelineMode.TRAIN
        assert ctx.config == {}
        assert ctx.metadata == {}
        assert ctx.models == {}
        assert ctx.metrics == {}

    def test_custom_init(self):
        ctx = PipelineContext(
            debug=DebugLevel.RELEASE,
            mode=PipelineMode.INFER,
            config={"key": "value"},
        )
        assert ctx.debug == DebugLevel.RELEASE
        assert ctx.mode == PipelineMode.INFER
        assert ctx.config == {"key": "value"}

    def test_model_storage(self):
        ctx = PipelineContext()
        ctx.set_model("bert", {"weights": [1, 2, 3]})
        assert ctx.get_model("bert") == {"weights": [1, 2, 3]}
        assert ctx.get_model("missing") is None

    def test_metric_logging(self):
        ctx = PipelineContext()
        ctx.log_metric("loss", 0.5)
        ctx.log_metric("loss", 0.3)
        ctx.log_metric("accuracy", 0.9)
        assert ctx.metrics["loss"] == [0.5, 0.3]
        assert ctx.metrics["accuracy"] == [0.9]
