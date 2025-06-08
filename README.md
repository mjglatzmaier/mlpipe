# mlpipe

**A professional, modular pipeline framework for machine learning workflows.**

---

`mlpipe` is a lightweight DAG-based pipeline library designed to accelerate AI/ML research and production workflows. With support for YAML configuration, runtime contexts, stage registries, model diagnostics, and plug-and-play component management, it enables fast prototyping and clean deployment of custom ML pipelines.

---

## Features

- **Modular DAG execution** — Build workflows from stages with dependency resolution.
- **YAML-driven pipeline configs** — Separate logic from configuration for reproducibility.
- **Dynamic stage registry** — Plug-in new stage classes with a simple decorator.
- **Runtime context & mode control** — Easily toggle between `train`, `infer`, `label`, etc.
- **Model caching & registry** — Avoid redundant loads; manage models globally.
- **Evaluation stubs & diagnostics** — Track metrics and log model diagnostics.
- **Auto-tuning scaffold** — Foundation for parameter sweeps or intelligent optimization.

---
