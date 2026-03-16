"""Example: load a pipeline definition from a YAML file."""

# Ensure stages are imported (registration happens at import time).
import examples.basic_pipeline  # noqa: F401  — registers Greeter & Uppercaser
from mlpipe import PipelineContext, PipelineExecutor
from mlpipe.utils.yaml_loader import load_pipeline_config


def main():
    stages = load_pipeline_config("examples/pipeline.yaml")
    ctx = PipelineContext()
    PipelineExecutor(stages).run(ctx)

    print(f"\nResult: {ctx.metadata}")


if __name__ == "__main__":
    main()
