"""Tests for batch-parallel pipeline execution."""

from mlpipe.utils.parallel_runner import run_pipeline_batch_stages


class TestParallelRunner:
    def test_batch_execution(self):
        pipeline = [
            {"name": "dummy", "stage": "DummyStage", "config": {"message": "batch"}},
        ]
        items = [{"id": i} for i in range(5)]
        results = run_pipeline_batch_stages(stages=pipeline, items=items, n_jobs=1)

        assert len(results) == 5
        for ctx in results:
            assert ctx.metadata["setup"] is True
            assert ctx.metadata["process"] is True
            assert ctx.metadata["item"]["id"] in range(5)

    def test_batch_with_dependencies(self):
        pipeline = [
            {"name": "s1", "stage": "DummyStage", "config": {"message": "a"}},
            {"name": "s2", "stage": "DummyStage", "after": "s1", "config": {"message": "b"}},
        ]
        items = [{"id": i} for i in range(3)]
        # n_jobs=1 avoids subprocess spawning where stages aren't registered.
        # For multi-process parallelism, stage modules must be importable in
        # worker processes (see parallel_runner docstrings).
        results = run_pipeline_batch_stages(stages=pipeline, items=items, n_jobs=1)
        assert len(results) == 3
