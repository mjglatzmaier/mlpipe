from core.stage import Stage, register_stage
# from sklearn.linear_model import LogisticRegression
# from managers.model_diagnostics import ModelDiagnostics

@register_stage("Trainer")
class Trainer(Stage):
    def setup(self, ctx): pass

    def process(self, ctx): pass
        # df = ctx.metadata["data"]
        # X = df.drop("label", axis=1)
        # y = df["label"]
        # model = LogisticRegression()
        # model.fit(X, y)
        # ctx.set_model("logreg", model)
        # diag = ModelDiagnostics().evaluate(model, X, y)
        # for k, v in diag.items():
        #     ctx.log_metric(k, v)

    def postprocess(self, ctx): pass