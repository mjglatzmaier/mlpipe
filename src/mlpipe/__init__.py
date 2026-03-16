"""
mlpipe — A lightweight DAG-based pipeline framework for ML workflows.

Define pipeline stages, wire them with YAML or Python dicts, and execute
them in topological order with optional joblib-based parallelism.
"""

__version__ = "0.5.0"
__author__ = "M.Glatzmaier"

from .core.context import PipelineContext
from .core.dag import PipelineExecutor
from .core.registry import registry
from .core.stage import Stage

__all__ = ["PipelineContext", "PipelineExecutor", "Stage", "registry"]
