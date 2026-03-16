"""Tests for the DAG-based PipelineExecutor."""

import pytest

from mlpipe.core.dag import PipelineExecutor


class TestPipelineExecutor:
    """Core executor tests using the registered DummyStage."""

    def test_single_stage_train(self, ctx_train):
        pipeline = [
            {"name": "dummy", "stage": "DummyStage", "config": {"message": "hi"}},
        ]
        executor = PipelineExecutor(pipeline)
        executor.run(ctx_train)

        assert ctx_train.metadata["setup"] is True
        assert ctx_train.metadata["process"] is True
        assert ctx_train.metadata["postprocess"] is True

    def test_single_stage_infer(self, ctx_infer):
        pipeline = [
            {"name": "dummy", "stage": "DummyStage", "config": {"message": "hello"}},
        ]
        executor = PipelineExecutor(pipeline)
        executor.run(ctx_infer)

        assert ctx_infer.metadata["infer_message"] == "hello"

    def test_stage_dependencies_ordering(self, ctx_train):
        """Stages with 'after' are executed in the correct order."""
        pipeline = [
            {"name": "step3", "stage": "DummyStage", "after": "step2"},
            {"name": "step1", "stage": "DummyStage"},
            {"name": "step2", "stage": "DummyStage", "after": "step1"},
        ]
        executor = PipelineExecutor(pipeline)
        # If this doesn't raise, topological sort is working
        executor.run(ctx_train)

    def test_missing_dependency_raises(self):
        pipeline = [
            {"name": "step1", "stage": "DummyStage", "after": "nonexistent"},
        ]
        with pytest.raises(ValueError, match="not defined"):
            PipelineExecutor(pipeline)

    def test_cycle_detection(self):
        pipeline = [
            {"name": "a", "stage": "DummyStage", "after": "b"},
            {"name": "b", "stage": "DummyStage", "after": "a"},
        ]
        with pytest.raises(ValueError, match="cycle"):
            PipelineExecutor(pipeline)

    def test_unregistered_stage_raises(self, ctx_train):
        pipeline = [
            {"name": "bad", "stage": "NoSuchStage"},
        ]
        executor = PipelineExecutor(pipeline)
        with pytest.raises(KeyError, match="not registered"):
            executor.run(ctx_train)

    def test_stage_config_isolation(self, ctx_train):
        """Each stage gets its own config; global ctx.config is untouched."""
        ctx_train.config = {"global": True}

        pipeline = [
            {"name": "s1", "stage": "DummyStage", "config": {"message": "first"}},
            {"name": "s2", "stage": "DummyStage", "after": "s1", "config": {"message": "second"}},
        ]
        executor = PipelineExecutor(pipeline)
        executor.run(ctx_train)

        # Global config should not have been overwritten
        assert ctx_train.config == {"global": True}


class TestYAMLPipeline:
    def test_load_and_run(self, ctx_infer):
        from mlpipe.utils.yaml_loader import load_pipeline_config

        stages = load_pipeline_config("tests/config/cfg_dummy.yaml")
        executor = PipelineExecutor(stages)
        executor.run(ctx_infer)

        assert ctx_infer.metadata["setup"] is True
        assert ctx_infer.metadata["process"] is True
        assert ctx_infer.metadata["postprocess"] is True
