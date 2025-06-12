import sys

class StageRegistry:
    def __init__(self):
        self._registry = {}

    def register_stage(self, name):
        def decorator(cls):
            self._registry[name] = cls
            return cls
        return decorator

    def get_stage_class(self, name):
        return self._registry[name]

    def get_registry(self):
        return self._registry

# Install a true singleton in sys.modules
_GLOBAL_REGISTRY_KEY = "_mlpipe_stage_registry"
if _GLOBAL_REGISTRY_KEY not in sys.modules:
    sys.modules[_GLOBAL_REGISTRY_KEY] = StageRegistry()

registry = sys.modules[_GLOBAL_REGISTRY_KEY]