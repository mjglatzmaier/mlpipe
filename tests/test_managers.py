"""Tests for the managers module."""


from mlpipe.managers.mgr_model import ModelManager
from mlpipe.managers.mgr_tuner import AutoTuner


class TestModelManager:
    def test_register_and_get(self):
        mgr = ModelManager()
        mgr.register("m1", {"type": "linear"})
        assert mgr.get("m1") == {"type": "linear"}
        assert mgr.get("missing") is None

    def test_lazy_load(self):
        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return "loaded_model"

        mgr = ModelManager()
        result1 = mgr.load("m", loader)
        result2 = mgr.load("m", loader)

        assert result1 == "loaded_model"
        assert result2 == "loaded_model"
        assert call_count == 1  # loader called only once

    def test_list_models(self):
        mgr = ModelManager()
        mgr.register("b", 2)
        mgr.register("a", 1)
        assert mgr.list_models() == ["a", "b"]


class TestAutoTuner:
    def test_suggest_returns_valid_config(self):
        tuner = AutoTuner({"lr": (0.001, 0.1), "batch_size": 32})
        config = tuner.suggest()

        assert 0.001 <= config["lr"] <= 0.1
        assert config["batch_size"] == 32

    def test_history_tracking(self):
        tuner = AutoTuner({"x": (0, 1)})
        tuner.suggest()
        tuner.suggest()
        assert len(tuner.history) == 2
