"""Minimal example: define stages and run a pipeline from Python."""

from mlpipe import PipelineContext, PipelineExecutor, Stage, registry

# --- Define two simple stages -------------------------------------------

@registry.register_stage("Greeter")
class Greeter(Stage):
    def setup(self, ctx):
        self.name = ctx.stage_config.get("name", "World")

    def process(self, ctx):
        ctx.metadata["greeting"] = f"Hello, {self.name}!"

    def postprocess(self, ctx):
        print(ctx.metadata["greeting"])


@registry.register_stage("Uppercaser")
class Uppercaser(Stage):
    def setup(self, ctx):
        pass

    def process(self, ctx):
        ctx.metadata["greeting"] = ctx.metadata["greeting"].upper()

    def postprocess(self, ctx):
        print(f"  → {ctx.metadata['greeting']}")


# --- Build and run the pipeline -----------------------------------------

def main():
    stages = [
        {"name": "greet",     "stage": "Greeter",    "config": {"name": "Engineer"}},
        {"name": "uppercase", "stage": "Uppercaser", "after": "greet"},
    ]

    ctx = PipelineContext()
    PipelineExecutor(stages).run(ctx)

    print(f"\nFinal greeting: {ctx.metadata['greeting']}")
    print(f"Metrics: {ctx.metrics}")


if __name__ == "__main__":
    main()
