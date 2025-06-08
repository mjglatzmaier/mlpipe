class MetricTracker:
    def __init__(self):
        self.metrics = {}

    def log(self, name, value):
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)

    def get(self, name):
        return self.metrics.get(name, [])

    def summary(self):
        return {k: sum(v)/len(v) if v else None for k, v in self.metrics.items()}