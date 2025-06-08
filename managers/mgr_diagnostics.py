class ModelDiagnostics:
    def evaluate(self, model, X, y):
        try:
            score = model.score(X, y)
        except Exception:
            score = None
        return {
            "accuracy": score,
            "n_features": getattr(model, "n_features_in_", None),
            "model_class": model.__class__.__name__
        }
