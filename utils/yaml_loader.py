import yaml

def load_pipeline_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config["pipeline"]