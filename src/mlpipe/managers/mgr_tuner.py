"""Lightweight random-search hyperparameter tuner."""

from __future__ import annotations

import random
from typing import Any


class AutoTuner:
    """Suggest hyperparameter configs via random search.

    Each key in *search_space* maps to either a ``(low, high)`` tuple
    (sampled uniformly) or a fixed value passed through as-is.

    Example::

        tuner = AutoTuner({"lr": (1e-5, 1e-2), "batch_size": 32})
        config = tuner.suggest()  # {"lr": 0.00387, "batch_size": 32}
    """

    def __init__(self, search_space: dict[str, Any]) -> None:
        self.search_space = search_space
        self.history: list[dict[str, Any]] = []

    def suggest(self) -> dict[str, Any]:
        """Return a randomly sampled configuration."""
        config = {}
        for key, spec in self.search_space.items():
            if isinstance(spec, (list, tuple)) and len(spec) == 2:
                config[key] = random.uniform(spec[0], spec[1])
            else:
                config[key] = spec
        self.history.append(config)
        return config
