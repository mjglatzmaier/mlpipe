class ModelManager:
    def __init__(self):
        self.models = {}

    def register(self, name, model):
        self.models[name] = model

    def get(self, name):
        return self.models.get(name)

    def load(self, name, loader_fn):
        if name not in self.models:
            self.models[name] = loader_fn()
        return self.models[name]