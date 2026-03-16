"""Pipeline mode and debug level enumerations."""

from enum import Enum, auto


class PipelineMode(Enum):
    """Operating mode for a pipeline run."""
    TRAIN = auto()
    INFER = auto()
    LABEL = auto()


class DebugLevel(Enum):
    """Controls verbosity / debug behaviour."""
    DEBUG = auto()
    RELEASE = auto()
