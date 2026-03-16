"""Global stage registry — maps string names to Stage subclasses."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .stage import Stage


class StageRegistry:
    """Singleton registry that maps stage names to their classes.

    Usage::

        from mlpipe.core.registry import registry

        @registry.register_stage("MyStage")
        class MyStage(Stage):
            ...

        cls = registry.get_stage_class("MyStage")
    """

    def __init__(self) -> None:
        self._registry: dict[str, type[Stage]] = {}

    def register_stage(self, name: str):
        """Class decorator that registers a :class:`Stage` under *name*."""
        def decorator(cls: type[Stage]) -> type[Stage]:
            self._registry[name] = cls
            return cls
        return decorator

    def get_stage_class(self, name: str) -> type[Stage]:
        """Return the stage class registered as *name*.

        Raises:
            KeyError: If *name* has not been registered.
        """
        if name not in self._registry:
            registered = ", ".join(sorted(self._registry)) or "(none)"
            raise KeyError(
                f"Stage '{name}' is not registered. "
                f"Registered stages: {registered}"
            )
        return self._registry[name]

    def list_stages(self) -> list[str]:
        """Return a sorted list of all registered stage names."""
        return sorted(self._registry)


# Module-level singleton — one registry per process.
registry = StageRegistry()
