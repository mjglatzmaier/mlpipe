# mlpipe

**A modular pipeline framework for machine learning workflows.**

---

`mlpipe` is a lightweight DAG-based pipeline library designed to accelerate AI/ML research and production workflows. With support for YAML configuration, runtime contexts, stage registries, model diagnostics, and plug-and-play component management, it enables fast prototyping and clean deployment of custom ML pipelines.

---

## Features

- Modular DAG execution engine with topological stage ordering
- YAML-driven configuration for reproducibility and flexibility
- Torch and ONNX runtime inference stages
- Logging, metric tracking, and model diagnostics
- Auto-tuning stubs and model registry support
- Parallel stage execution

---

## Environment Setup (Conda + VS Code)

To use `mlpipe` on Linux with BLAS acceleration and optional CUDA for Torch:

### 1. Clone the repository
```bash
git clone https://github.com/yourname/mlpipe.git
cd mlpipe
```

### 2. Create and activate Conda environment
```bash
conda create -n mlpipe python=3.10 -y
conda activate mlpipe
```

### 3. Install dependencies
Install BLAS-optimized numpy and PyTorch (with or without CUDA):
```bash
# Use conda-forge for better binary compatibility
conda install -c conda-forge numpy pandas scikit-learn pyyaml networkx loguru

# CPU-only PyTorch
conda install pytorch torchvision torchaudio cpuonly -c pytorch

# OR for CUDA support (e.g., CUDA 11.8)
# conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# Install ONNX Runtime
pip install onnxruntime

# Optional: For ONNX GPU support
# pip install onnxruntime-gpu
```

### 4. Enable VS Code integration (optional)
```bash
conda install -c conda-forge ipykernel
python -m ipykernel install --user --name=mlpipe
```
Then in VS Code:
- Open Command Palette → "Python: Select Interpreter" → Choose `mlpipe`

### 5. Run example pipeline
```bash
python examples/run_pipeline_yaml.py
```

---

## Requirements File (optional)
You may include this in `requirements.txt` if using `pip`:
```txt
numpy
pandas
scikit-learn
pyyaml
networkx
loguru
torch
onnxruntime
```
Use it with:
```bash
pip install -r requirements.txt
```

---
