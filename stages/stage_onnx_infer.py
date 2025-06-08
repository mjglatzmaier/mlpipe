from core.stage import Stage, register_stage
import onnxruntime as ort
import numpy as np

@register_stage("OnnxInference")
class OnnxInference(Stage):
    def setup(self, ctx):
        model_path = ctx.config["model_path"]
        self.session = ort.InferenceSession(model_path)

    def process(self, ctx):
        inputs = ctx.metadata[ctx.config["input_key"]]
        input_name = self.session.get_inputs()[0].name
        result = self.session.run(None, {input_name: inputs.astype(np.float32)})
        ctx.metadata[ctx.config["output_key"]] = result[0]

    def postprocess(self, ctx):
        pass
