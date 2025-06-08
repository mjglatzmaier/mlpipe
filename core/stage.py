from abc import ABC, abstractmethod

_STAGE_REGISTRY = {}

def register_stage(name):
    def decorator(cls):
        _STAGE_REGISTRY[name] = cls
        return cls
    return decorator

def get_stage_class(name):
    return _STAGE_REGISTRY[name]

class Stage(ABC):
    @abstractmethod
    def setup(self, ctx): pass

    @abstractmethod
    def process(self, ctx): pass

    @abstractmethod
    def postprocess(self, ctx): pass