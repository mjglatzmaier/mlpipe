"""Batch-parallel pipeline execution using joblib."""

from __future__ import annotations

from typing import Any

from joblib import Parallel, delayed

from ..core.context import PipelineContext
from ..core.dag import PipelineExecutor
from .yaml_loader import load_pipeline_config


def run_pipeline(config_path: str, item: Any) -> PipelineContext:
    """Run a single pipeline from a YAML config file.

    Args:
        config_path: Path to a YAML pipeline definition.
        item: An arbitrary object stored in ``ctx.metadata["item"]``.

    Returns:
        The :class:`PipelineContext` after execution.
    """
    stages = load_pipeline_config(config_path)
    return run_pipeline_stages(stages, item)


def run_pipeline_stages(stages: list[dict[str, Any]], item: Any) -> PipelineContext:
    """Run a single pipeline from an in-memory stage list.

    Args:
        stages: List of stage descriptor dicts.
        item: An arbitrary object stored in ``ctx.metadata["item"]``.

    Returns:
        The :class:`PipelineContext` after execution.
    """
    ctx = PipelineContext()
    ctx.metadata["item"] = item
    executor = PipelineExecutor(stages)
    executor.run(ctx)
    return ctx


def run_pipeline_batch(
    config_path: str,
    items: list[Any],
    n_jobs: int = 4,
) -> list[PipelineContext]:
    """Run a pipeline over many items in parallel (YAML config).

    Args:
        config_path: Path to a YAML pipeline definition.
        items: List of items to process (one pipeline run each).
        n_jobs: Number of parallel workers (passed to joblib).

    Returns:
        A list of :class:`PipelineContext` results, one per item.
    """
    return Parallel(n_jobs=n_jobs)(
        delayed(run_pipeline)(config_path, item) for item in items
    )


def run_pipeline_batch_stages(
    stages: list[dict[str, Any]],
    items: list[Any],
    n_jobs: int = 4,
) -> list[PipelineContext]:
    """Run a pipeline over many items in parallel (in-memory stages).

    Args:
        stages: List of stage descriptor dicts.
        items: List of items to process (one pipeline run each).
        n_jobs: Number of parallel workers (passed to joblib).

    Returns:
        A list of :class:`PipelineContext` results, one per item.
    """
    return Parallel(n_jobs=n_jobs)(
        delayed(run_pipeline_stages)(stages, item) for item in items
    )
