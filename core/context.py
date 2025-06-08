class PipelineContext:
    def __init__(self, mode='debug', stage='train', config=None):
        self.mode = mode
        self.stage = stage
        self.config = config or {}
        self.metadata = {}
        self.models = {}
        self.metrics = {}
        self.flags = {}

    def set_model(self, name, model):
        self.models[name] = model

    def get_model(self, name):
        return self.models.get(name)

    def log_metric(self, name, value):
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)

    def set_flag(self, key, value=True):
        self.flags[key] = value

    def get_flag(self, key, default=False):
        return self.flags.get(key, default)