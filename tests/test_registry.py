"""Tests for the StageRegistry."""

import pytest

from mlpipe.core.registry import StageRegistry
from mlpipe.core.stage import Stage


class TestStageRegistry:
    def test_register_and_retrieve(self):
        reg = StageRegistry()

        @reg.register_stage("TestStage")
        class TestStage(Stage):
            def setup(self, ctx): pass
            def process(self, ctx): pass
            def postprocess(self, ctx): pass

        assert reg.get_stage_class("TestStage") is TestStage

    def test_missing_stage_raises(self):
        reg = StageRegistry()
        with pytest.raises(KeyError, match="not registered"):
            reg.get_stage_class("NoSuchStage")

    def test_list_stages(self):
        reg = StageRegistry()

        @reg.register_stage("B")
        class B(Stage):
            def setup(self, ctx): pass
            def process(self, ctx): pass
            def postprocess(self, ctx): pass

        @reg.register_stage("A")
        class A(Stage):
            def setup(self, ctx): pass
            def process(self, ctx): pass
            def postprocess(self, ctx): pass

        assert reg.list_stages() == ["A", "B"]
