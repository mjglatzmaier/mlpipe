# mlpipe

[![CI](https://github.com/mjglatzmaier/mlpipe/actions/workflows/ci.yml/badge.svg)](https://github.com/mjglatzmaier/mlpipe/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**A lightweight DAG-based pipeline framework for ML workflows.**

Define stages, wire them with YAML or Python dicts, and execute them in
topological order — with optional parallel batch processing via joblib.

```
pip install -e .                  # core (networkx, pyyaml, loguru, joblib)
pip install -e ".[ml]"            # + numpy, pandas, scikit-learn
pip install -e ".[torch]"         # + PyTorch
pip install -e ".[dev]"           # + pytest, ruff
```

---

## Quick Start

### 1. Define a stage

```python
from mlpipe.core.stage import Stage
from mlpipe.core.registry import registry

@registry.register_stage("Normalize")
class Normalize(Stage):
    def setup(self, ctx):
        self.method = ctx.stage_config.get("method", "minmax")

    def process(self, ctx):
        data = ctx.metadata["data"]
        if self.method == "minmax":
            ctx.metadata["data"] = (data - data.min()) / (data.max() - data.min())

    def postprocess(self, ctx):
        ctx.log_metric("normalize_method", self.method)
```

### 2. Build a pipeline (Python)

```python
from mlpipe import PipelineContext, PipelineExecutor

stages = [
    {"name": "load",      "stage": "DataLoader"},
    {"name": "normalize", "stage": "Normalize", "after": "load",
     "config": {"method": "minmax"}},
    {"name": "train",     "stage": "Trainer",   "after": "normalize"},
]

ctx = PipelineContext()
PipelineExecutor(stages).run(ctx)
```

### 3. Or use YAML

```yaml
# pipeline.yaml
pipeline:
  - name: load
    stage: DataLoader
  - name: normalize
    stage: Normalize
    after: load
    config:
      method: minmax
  - name: train
    stage: Trainer
    after: normalize
```

```python
from mlpipe.utils.yaml_loader import load_pipeline_config
from mlpipe import PipelineContext, PipelineExecutor

stages = load_pipeline_config("pipeline.yaml")
PipelineExecutor(stages).run(PipelineContext())
```

### 4. Batch-parallel execution

```python
from mlpipe.utils.parallel_runner import run_pipeline_batch_stages

items = [{"file": f"data_{i}.csv"} for i in range(100)]
results = run_pipeline_batch_stages(stages, items, n_jobs=4)
```

---

## Architecture

```
PipelineContext         Mutable state bag carried through every stage
    ├── config          Global config (never overwritten by the executor)
    ├── stage_config    Per-stage config (set by the executor before each stage)
    ├── metadata        Free-form dict for inter-stage data passing
    ├── models          Named model storage
    └── metrics         Named metric lists

Stage (ABC)             Base class — implement setup / process / postprocess
StageRegistry           Decorator-based name → class mapping
PipelineExecutor        Builds a networkx DAG, runs stages in topological order
```

### Stage lifecycle

For each stage in topological order, the executor calls:

1. **`setup(ctx)`** — initialise resources, read config from `ctx.stage_config`
2. **`process(ctx)`** — core logic (training, inference, transforms, etc.)
3. **`postprocess(ctx)`** — log results, persist artifacts, clean up

### Key design decisions

- **`ctx.stage_config` vs `ctx.config`**: The executor sets `ctx.stage_config`
  per-stage from the `config` dict in the stage descriptor. `ctx.config` is
  global and never touched by the executor — use it for cross-cutting settings.
- **Stage registration is import-driven**: stages are registered when their
  module is imported (via the `@registry.register_stage` decorator). Ensure
  stage modules are imported before building a `PipelineExecutor`.

---

## Extras

| Module | Description |
|---|---|
| `managers.mgr_model` | `ModelManager` — named model cache with lazy loading |
| `managers.mgr_tuner` | `AutoTuner` — random-search hyperparameter suggestions |
| `utils.logging` | `configure_logging()` — opt-in file logging via loguru |
| `utils.mode` | `PipelineMode` (TRAIN/INFER/LABEL) and `DebugLevel` enums |

---

## Development

```bash
pip install -e ".[dev]"
pytest                            # run tests
ruff check .                      # lint
ruff format .                     # format
```

---

## License

MIT — see [LICENSE](LICENSE).
