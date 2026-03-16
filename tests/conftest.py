"""Pytest fixtures shared across all mlpipe tests."""

import pytest

# Ensure the DummyStage is registered before any test that needs it.
import tests.test_stages.stage_dummy  # noqa: F401
from mlpipe.core.context import PipelineContext
from mlpipe.utils.mode import PipelineMode


@pytest.fixture
def ctx_train() -> PipelineContext:
    """A fresh PipelineContext in TRAIN mode (the default)."""
    return PipelineContext()


@pytest.fixture
def ctx_infer() -> PipelineContext:
    """A fresh PipelineContext in INFER mode."""
    return PipelineContext(mode=PipelineMode.INFER)
