from joblib import Parallel, delayed
from core.context import PipelineContext
from core.dag import PipelineExecutor
from utils.yaml_loader import load_pipeline_config
from core.stage import Stage, register_stage
from core.context import PipelineContext
from tests.test_stages.stage_dummy import DummyStage 

def run_pipeline(config_path : str, item_config):
    stages = load_pipeline_config(config_path)
    ctx = PipelineContext()
    ctx.metadata["item"] = item_config
    executor = PipelineExecutor(stages)
    executor.run(ctx)
    return ctx

def run_pipeline_stages(stages : list[dict], item_config):
    ctx = PipelineContext()
    ctx.metadata["item"] = item_config
    executor = PipelineExecutor(stages)
    executor.run(ctx)
    return ctx

def run_pipeline_batch(config_path : str, item_list, n_jobs=4):
    return Parallel(n_jobs=n_jobs)(
        delayed(run_pipeline)(config_path, item) for item in item_list
    )

def run_pipeline_batch_stages(stages : list[dict], item_list, n_jobs=4):
    return Parallel(n_jobs=n_jobs)(
        delayed(run_pipeline_stages)(stages, item) for item in item_list
    )

# TODO
# def batchify(data, batch_size):
#     for i in range(0, len(data), batch_size):
#         yield data[i:i + batch_size]