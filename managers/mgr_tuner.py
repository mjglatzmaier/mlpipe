import random

class AutoTuner:
    def __init__(self, search_space):
        self.search_space = search_space

    def suggest(self):
        return {k: random.uniform(*v) if isinstance(v, (list, tuple)) and len(v) == 2 else v
                for k, v in self.search_space.items()}

    def update(self, feedback):
        pass