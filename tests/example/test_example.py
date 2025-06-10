from core.context import PipelineContext
from core.dag import PipelineExecutor
from test_register import register_tests

# Import stages
from tests.test_stages.stage_dummy import DummyStage

def test_simple_execution():
    pipeline = [
        {
            "name": "dummy",
            "stage": "DummyStage",
            "config": {
                "debug" : True,
                "message": "Hello from config!"
            }
        }
    ]
    ctx = PipelineContext()
    executor = PipelineExecutor(pipeline)
    executor.run(ctx)
    print("Pipeline executed successfully")
    assert ctx.metadata.get("setup") is True, "Setup not called"
    assert ctx.metadata.get("process") is True, "Process not called"
    assert ctx.metadata.get("postprocess") is True, "Postprocess not called"

def test_load_pipeline_from_config():
    from utils.yaml_loader import load_pipeline_config
    from core.context import PipelineContext
    from core.dag import PipelineExecutor
    stages = load_pipeline_config("tests/config/cfg_dummy.yaml")
    ctx = PipelineContext()
    executor = PipelineExecutor(stages)
    executor.run(ctx)
    assert ctx.metadata.get("setup") is True, "Setup not called"
    assert ctx.metadata.get("process") is True, "Process not called"
    assert ctx.metadata.get("postprocess") is True, "Postprocess not called"

def test_parallel_execution():
    from utils.parallel_runner import run_pipeline_batch_stages
    pipeline = [
        {"name": "dummy1", "stage": "DummyStage", "config": {"message": "msg1", "sleep": 0.1}},
        {"name": "dummy2", "stage": "DummyStage", "after": "dummy1", "config": {"message": "msg2", "sleep": 0.2}},
        {"name": "dummy3", "stage": "DummyStage", "after": "dummy2", "config": {"message": "msg3", "sleep": 0.3}},
        {"name": "dummy4", "stage": "DummyStage", "after": "dummy3", "config": {"message": "msg4", "sleep": 0.4}},
        {"name": "dummy5", "stage": "DummyStage", "after": "dummy4", "config": {"message": "msg5", "sleep": 0.5}}
    ]
    class DummyItem:
        def __init__(self, name):
            self.name = name
    # Make a list of "items" to process
    items = [DummyItem(f"item_{i}") for i in range(10)]

    # Run the pipeline in parallel
    # For parallel jobs, running outside the debugger in VS code removes joblib errors
    run_pipeline_batch_stages(stages=pipeline, item_list=items, n_jobs=1)

    # Check metadata for each stage
    # assert ctx.metadata.get("dummy1") is not None, "Metadata for dummy1 not found"
    # assert ctx.metadata.get("dummy2") is not None, "Metadata for dummy2 not found"
    # assert ctx.metadata.get("dummy3") is not None, "Metadata for dummy3 not found"
    # assert ctx.metadata.get("dummy4") is not None, "Metadata for dummy4 not found"
    # assert ctx.metadata.get("dummy5") is not None, "Metadata for dummy5 not found"

def test_stage_dependencies():
    pass
register_tests(locals())