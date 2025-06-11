from utils.mode import DebugLevel, PipelineMode

class PipelineContext:
    def __init__(self, debug=DebugLevel.DEBUG, mode=PipelineMode.TRAIN, config=None):
        self.debug = debug
        self.mode = mode
        self.config = config or {}
        self.metadata = {}
        self.models = {}
        self.metrics = {}

    def set_model(self, name, model):
        self.models[name] = model

    def get_model(self, name):
        return self.models.get(name)

    def log_metric(self, name, value):
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)
