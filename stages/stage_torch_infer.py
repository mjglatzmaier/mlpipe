from core.stage import Stage, register_stage
import torch
import numpy as np

@register_stage("TorchInference")
class TorchInference(Stage):
    def setup(self, ctx):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.load(ctx.config["model_path"])
        self.model.to(self.device)
        self.model.eval()

    def process(self, ctx):
        data = torch.tensor(ctx.metadata[ctx.config["input_key"]], dtype=torch.float32).to(self.device)
        with torch.no_grad():
            out = self.model(data).cpu().numpy()
        ctx.metadata[ctx.config["output_key"]] = out

    def postprocess(self, ctx):
        pass