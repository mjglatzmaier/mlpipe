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

### 2. Clean up and prepare Conda environment
```bash
# Remove any previous broken installs
conda clean --all -y
conda config --set channel_priority strict
conda config --add channels conda-forge
conda config --add channels pytorch
conda config --add channels nvidia
```

### 3. Create and activate Conda environment (with GPU support)
```bash
conda create -n mlpipe python=3.11 -y
conda activate mlpipe

conda install pytorch torchvision torchaudio pytorch-cuda=12.1 \
    -c pytorch -c nvidia -c conda-forge --override-channels
```

### 4. Verify GPU support
```bash
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

### 5. Install dependencies
Install BLAS-optimized numpy and PyTorch (with or without CUDA):
```bash
# Use conda-forge for better binary compatibility
conda install -c conda-forge numpy pandas scikit-learn pyyaml networkx loguru

# CPU-only PyTorch
# conda install pytorch torchvision torchaudio cpuonly -c pytorch

# Install ONNX Runtime
# pip install onnxruntime

# Optional: For ONNX GPU support
pip install onnxruntime-gpu
```

### 6. Enable VS Code integration (optional)
```bash
conda install -c conda-forge ipykernel
python -m ipykernel install --user --name=mlpipe
```
Then in VS Code:
- Open Command Palette → "Python: Select Interpreter" → Choose `mlpipe`

### 7. Run example pipeline
```bash
python examples/run_pipeline_yaml.py
```

---

Install with:
```bash
pip install -e ./mlpipe
```

---

## License
MIT License
