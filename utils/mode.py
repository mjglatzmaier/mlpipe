from enum import Enum, auto

class PipelineMode(Enum):
    TRAIN = auto()
    INFER = auto()
    LABEL = auto()

class DebugLevel(Enum):
    DEBUG = auto()
    RELEASE = auto()