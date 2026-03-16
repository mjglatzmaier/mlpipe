"""Base class for all pipeline stages."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context import PipelineContext


class Stage(ABC):
    """Abstract base for a pipeline stage.

    Every stage goes through three phases, called in order by the
    :class:`~mlpipe.core.dag.PipelineExecutor`:

    1. **setup** — initialise resources, validate config.
    2. **process** — perform the main work.
    3. **postprocess** — clean up, log results, persist artefacts.

    Subclass this and register with ``@registry.register_stage("Name")``.
    """

    @abstractmethod
    def setup(self, ctx: PipelineContext) -> None:
        """Prepare the stage (called before ``process``)."""

    @abstractmethod
    def process(self, ctx: PipelineContext) -> None:
        """Run the core logic of the stage."""

    @abstractmethod
    def postprocess(self, ctx: PipelineContext) -> None:
        """Finalise results (called after ``process``)."""
