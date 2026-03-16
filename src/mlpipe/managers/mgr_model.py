"""Simple named-model store with lazy loading support."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class ModelManager:
    """Registry for named models with optional lazy loading.

    Use this when you need a shared model cache outside of
    :class:`~mlpipe.core.context.PipelineContext` (e.g. across
    multiple pipeline runs or in a serving layer).

    Example::

        mgr = ModelManager()
        mgr.register("bert", my_model)
        mgr.load("slow_model", lambda: load_from_disk("model.pt"))
    """

    def __init__(self) -> None:
        self._models: dict[str, Any] = {}

    def register(self, name: str, model: Any) -> None:
        """Store *model* under *name*, replacing any existing entry."""
        self._models[name] = model

    def get(self, name: str) -> Any | None:
        """Return the model registered as *name*, or ``None``."""
        return self._models.get(name)

    def load(self, name: str, loader_fn: Callable[[], Any]) -> Any:
        """Return the model for *name*, calling *loader_fn* on first access."""
        if name not in self._models:
            self._models[name] = loader_fn()
        return self._models[name]

    def list_models(self) -> list[str]:
        """Return a sorted list of registered model names."""
        return sorted(self._models)
