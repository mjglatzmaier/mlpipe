"""Pipeline execution context — shared state passed through every stage."""

from __future__ import annotations

from typing import Any

from ..utils.mode import DebugLevel, PipelineMode


class PipelineContext:
    """Mutable bag of state carried through a pipeline run.

    Attributes:
        debug:    Current debug level (DEBUG or RELEASE).
        mode:     Pipeline mode (TRAIN, INFER, or LABEL).
        config:   Global configuration dict (not overwritten per-stage).
        metadata: Arbitrary key/value store for inter-stage communication.
        models:   Named model storage (e.g. loaded weights).
        metrics:  Named metric lists for tracking values over time.
    """

    def __init__(
        self,
        debug: DebugLevel = DebugLevel.DEBUG,
        mode: PipelineMode = PipelineMode.TRAIN,
        config: dict[str, Any] | None = None,
    ) -> None:
        self.debug = debug
        self.mode = mode
        self.config: dict[str, Any] = config or {}
        self.metadata: dict[str, Any] = {}
        self.models: dict[str, Any] = {}
        self.metrics: dict[str, list[Any]] = {}

    def set_model(self, name: str, model: Any) -> None:
        """Store a model by name."""
        self.models[name] = model

    def get_model(self, name: str) -> Any | None:
        """Retrieve a model by name, or ``None`` if not found."""
        return self.models.get(name)

    def log_metric(self, name: str, value: Any) -> None:
        """Append *value* to the named metric list."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)
