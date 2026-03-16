"""YAML pipeline configuration loader."""

from __future__ import annotations

from typing import Any

import yaml


def load_pipeline_config(path: str) -> list[dict[str, Any]]:
    """Load a pipeline definition from a YAML file.

    The YAML file must contain a top-level ``pipeline`` key whose value
    is a list of stage descriptors.

    Args:
        path: Path to the YAML configuration file.

    Returns:
        A list of stage descriptor dicts.

    Raises:
        FileNotFoundError: If *path* does not exist.
        KeyError: If the YAML lacks a ``pipeline`` key.
    """
    with open(path) as f:
        config = yaml.safe_load(f)

    if "pipeline" not in config:
        raise KeyError(
            f"YAML config at '{path}' is missing a top-level 'pipeline' key."
        )

    return config["pipeline"]
