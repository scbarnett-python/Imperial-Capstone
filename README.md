# Black-Box Optimisation Capstone Project

[![GitHub Repo](https://img.shields.io/badge/GitHub-scbarnett--python%2FImperial--Capstone-181717?logo=github&logoColor=white)](https://github.com/scbarnett-python/Imperial-Capstone)

## Project Overview

This project applies Bayesian Optimisation (BO) to maximise the outputs of eight unknown black-box functions using a limited evaluation budget. The underlying mathematical forms of the functions are completely hidden — optimisation decisions must be made solely from observed input-output data and a restricted number of weekly queries.

Gaussian Process (GP) surrogate models are used to learn the behaviour of each function from a small initial dataset, and acquisition functions are used to recommend future query locations. By iteratively updating beliefs about the response surface as new observations arrive, the project seeks to efficiently identify high-performing input combinations while operating under strict information and budget constraints.

This problem is representative of real-world applications in machine learning and engineering where evaluations are expensive, data is scarce, and the underlying input-output relationships are unknown. It is also directly relevant to quantitative finance, where similar challenges arise in identifying top-performing funds, constructing portfolios, or evaluating tail-risk hedging strategies — domains where the return-generating process is hidden, observations are noisy, and resources are limited.

---

## Project Documentation

| Document | Description | Link |
|----------|-------------|------|
| Datasheet | Documents the initial and weekly datasets: provenance, collection process, per-function structure, known limitations (noise, non-stationarity), and intended use | [BBO_Capstone_Datasheet.md](./BBO_Capstone_Datasheet.md) ([.docx](./BBO_Capstone_Datasheet.docx)) |
| Model Card | Documents the GP surrogate models: architecture, kernel choices per function, training/fitting process, intended use, and evaluation limitations | [BBO_Capstone_Model_Card.md](./BBO_Capstone_Model_Card.md) ([.docx](./BBO_Capstone_Model_Card.docx)) |
| Readme (Word) | Word-format mirror of this file | [Readme.docx](./Docs/Readme.docx) |

---

## Repository Structure

> **GitHub status:** the full project structure below (notebooks, data, utilities, figures, and `Docs/`) is pushed to GitHub. A `Notes/` folder also exists locally for private working documents (draft write-ups, reflections, AI-assistance notes) and is excluded from GitHub via `.gitignore` — it is not shown below. Auto-generated housekeeping folders (`.ipynb_checkpoints/`, `anaconda_projects/`, `__pycache__/`) are also omitted for clarity.

```
├── README.md
├── BBO_Capstone_Datasheet.docx
├── BBO_Capstone_Datasheet.md
├── BBO_Capstone_Model_Card.docx
├── BBO_Capstone_Model_Card.md
├── Capstone Project.ipynb           # Main notebook
├── Function_1.ipynb                 # Per-function GP modelling and acquisition notebooks
├── Function_2.ipynb
├── Function_3.ipynb
├── function_4.ipynb
├── Function_5.ipynb
├── Function_6.ipynb
├── Function_7.ipynb
├── Function_8.ipynb
├── Function_Temp.ipynb              # Scratch/testing notebook
├── Update_Data_Points.ipynb         # Central merging notebook: loads initial + weekly data
├── Capstone Project FAQs-1.pdf      # Project specification and FAQ
├── scipy-clean-full.yml             # Conda environment spec
├── Function1_progress_highwater.png
│
├── Function MD/                  # Per-function state: versioned markdown summary files
│   ├── Function_1_Summary.md
│   ├── Function_2_Summary.md
│   └── ... (through Function_8_Summary.md)
│
├── Docs/                         # Public project documentation
│   └── Readme.docx                # Word-format mirror of this file
│
├── Data/                         # Per-function evaluated points — full merged dataset + transform logs
│   ├── function_1/
│   │   ├── initial_inputs.npy / initial_outputs.npy
│   │   ├── initial_inputs_test.npy / initial_outputs_test.npy
│   │   ├── merged_inputs.npy / merged_outputs.npy
│   │   ├── input.csv / output.csv
│   │   └── y_transformations*.csv
│   └── ... (function_2 through function_8, same layout)
│
├── initial_data/                 # ⚠ status TBC — overlaps with Data/, see note below
│   ├── function_1/
│   │   ├── initial_inputs.npy / initial_outputs.npy
│   │   └── output.csv (+ y_transformations.csv for some functions)
│   └── ... (function_2 through function_8)
│
├── Figures/                      # Output visualisations: sigma maps, straddle maps, projection matrices
│   ├── Function1_sigma_map.png
│   ├── Function1_straddle_map.png
│   ├── Function1_exploration_signal.png
│   ├── Function2_exploration_signal.png
│   ├── Function2_sigma_map.png
│   ├── Function4_projection_matrix.png
│   ├── Function5_projection_matrix.png
│   ├── Function6_projection_matrix.png
│   ├── Function7_projection_matrix.png
│   ├── Function8_projection_matrix.png
│   └── ... (iteration/results snapshots)
│
├── Results/                      # Evaluated data tracking
│   └── Data Points.xlsx
│
├── Scratch/                      # Exploratory notebooks and test scripts (not production)
│   ├── Capstone Project ENV.ipynb
│   ├── MatrixMathsTest.ipynb
│   └── test.py
│
├── Utils/                        # Custom acquisition and plotting utilities
│   ├── imse_acquisition.py
│   ├── plot_input_pairs.py
│   └── plot_progress.py
│
└── Weekly_updates/                # Weekly submission inputs and returned outputs
    ├── w1_inputs.txt / w1_outputs.txt
    ├── w2_inputs.txt / w2_outputs.txt
    └── ... (through w9)
```

**⚠ Open item — `Data/` vs `initial_data/`:** both folders currently exist with overlapping per-function files. `Data/` (formerly `initial_data/`, renamed for clarity) holds the fuller working set, including `merged_*.npy` and test/transform files. `initial_data/` still exists alongside it with an older, smaller file set. Status of `initial_data/` (stale copy to be removed vs. still in use) is unresolved — flag when confirmed and this section will be updated.

**Data flow:** `Update_Data_Points.ipynb` reads `./Data/{function_name}/initial_inputs.npy` and `initial_outputs.npy`, then appends weekly results from `./Weekly_updates/{week}_inputs.txt` and `./Weekly_updates/{week}_outputs.txt` to produce the full X/y dataset used in the per-function notebooks (`Function_1.ipynb`–`Function_8.ipynb`).

---

## Function Summary

| Function | Dims | Domain | Best y (to date) | Active Acquisition |
|----------|------|--------|------------------|--------------------|
| 1 | 2D | [0,1]² | — | Straddle (level-set) |
| 2 | 2D | [0,1]² | 0.633 | EI + IMSE (coverage) |
| 3 | 3D | [0,1]³ | −0.00898 | EI (x3 ≤ 0.55 constraint) |
| 4 | 4D | [0,1]⁴ | −0.0424 | UCB / max-variance probe |
| 5 | 4D | [0,1]⁴ | 4577 | EI (near (1,1,1,1) corner) |
| 6 | 5D | [0,1]⁵ | −0.6245 | EI (isotropic kernel) |
| 7 | 6D | [0,1]⁶ | 1.5237 | EI (capped-ARD kernel) |
| 8 | 8D | [0,1]⁸ | 9.901 | EI (widened-ARD kernel) |

---

## Challenge Objectives

The goal is to **maximise** each black-box function. For every function, the objective is to find the input vector that produces the largest possible output value.

Key constraints:

- **Limited query budget:** Each query must be chosen carefully; total evaluations per function are strictly bounded.
- **Weekly response delay:** Only one new query can be submitted per function per week. Mistakes cannot be corrected immediately.
- **Unknown function structure:** The mathematical form of each function is hidden. Behaviour must be inferred solely from observed input-output pairs.
- **High-dimensional inputs:** Functions range from 2D to 8D, making optimisation increasingly difficult as dimensionality grows.
- **Exploration vs exploitation trade-off:** Queries must balance searching unexplored regions against refining areas already believed to be near the optimum.
- **Model uncertainty:** With relatively few observations, the surrogate may be inaccurate in regions far from existing data.

---

## Technical Approach

### Surrogate Model

Gaussian Process Regression (GPR) via `scikit-learn`'s `GaussianProcessRegressor`. Kernel selection follows a two-stage protocol:

1. **Isotropic vs ARD:** Chosen by AIC/BIC given current data size and dimensionality. Isotropic preferred at small n relative to dimension; ARD adopted when per-dimension structure is statistically supported.
2. **Length scale stability:** ARD instability (seed-dependent pinning at bounds) is resolved by capping `length_scale_bounds`. Cap values are calibrated per function — the (0.05, 2.0) default used for Functions 6–7 was widened to (0.05, 20) for Function 8, where genuine long length scales exist.

### Acquisition Functions

| Acquisition | When used |
|-------------|-----------|
| Expected Improvement (EI) | Standard exploitation/exploration balance; default choice |
| Upper Confidence Bound (UCB) | Multi-peak landscapes; deliberate coverage probes |
| Straddle / Level-Set | Threshold detection problems (Function 1: weak-source detection) |
| IMSE / Active Learning Cohn | Principled space-filling when stationary kernel coverage is biased (Function 2) |

### Key Methodological Decisions

- **ARD instability fix:** Cap `length_scale_bounds` rather than falling back to isotropic. Uncapped ARD (e.g. bounds (1e-3, 1e3)) produces highly seed-dependent fits. Capping at (0.05, 2.0) eliminates pathological local optima for most functions; cap must be calibrated per problem.
- **EI signal diagnosis:** Positive improvement term = exploitation-driven EI (meaningful signal). Negative improvement term = pure uncertainty-driven EI (weak signal — consider raising xi or switching acquisition).
- **High-dimensional candidate sampling:** Plain random sampling (10k points) is too sparse for 8D EI optimisation. Quasi-random (Sobol / LHS) sampling via `scipy.stats.qmc` used for Functions 7–8.
- **Radial correlation analysis:** `corr(y, distance_from_best)` efficiently diagnoses unimodality without full landscape mapping.
- **Straddle boundary margin:** Raw straddle is pulled to domain corners by extrapolation variance without `boundary_margin` and `exclude_radius` — these parameters are load-bearing.

---

## Python Environment

### Create and activate environment

```bash
conda create --prefix D:\conda-envs\bo-clean python=3.10 numpy scipy scikit-learn jupyter matplotlib ipykernel -y
conda activate D:\conda-envs\bo-clean
```

> **Windows note:** Always activate the environment explicitly from Anaconda Prompt before launching Jupyter. Cross-environment DLL contamination can cause MKL crashes if activation is skipped.

### Register as Jupyter kernel

```bash
python -m ipykernel install --user --name bo-clean --display-name "Python (bo-clean)"
```

### Optional packages

```bash
pip install tensorflow       # if needed for neural network baselines
pip install mlxtend          # pip preferred over conda-forge on Windows
```

---

## Libraries and Packages

| Library | Role |
|---------|------|
| `scikit-learn` | `GaussianProcessRegressor`, kernel composition, marginal likelihood optimisation |
| `numpy` | Array operations, data management |
| `scipy` | Optimisation (`minimize`), quasi-random sampling (`stats.qmc`) |
| `matplotlib` | Visualisation: sigma maps, straddle maps, acquisition landscapes |

**`Utils/imse_acquisition.py`** — custom IMSE/ALC acquisition implementing the integrated variance-reduction criterion with Latin Hypercube candidate/reference sampling and a kriging-believer heuristic for sequential multi-point selection.

**Trade-off considered:** GPyTorch would offer greater flexibility for custom kernels and larger datasets. scikit-learn was retained for its simplicity, stability, and suitability to the dataset sizes (n < 100 per function) encountered in this project.

---

## Per-Function State

Canonical per-function state (kernel parameters, current best point, acquisition strategy, open questions) is maintained as versioned markdown files in `Function MD/`. These are updated after each weekly submission cycle and serve as the primary living documentation alongside this README.
