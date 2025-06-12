from abc import ABC, abstractmethod

class Stage(ABC):
    @abstractmethod
    def setup(self, ctx): pass

    @abstractmethod
    def process(self, ctx): pass

    @abstractmethod
    def postprocess(self, ctx): pass