# Student Performance Analytics

Comprehensive, reproducible analysis of the UCI student performance datasets. The repo includes preprocessing pipelines, exploratory notebooks, supervised models (regression/classification), unsupervised clustering, and utilities to automatically capture plots and reports.

![Student Performance Overview](Header.png)

## Contents
- `data/raw/`: Original UCI CSVs (`student-mat.csv`, `student-por.csv`) plus metadata and archives.
- `data/processed/`: Feature matrices produced by the preprocessing pipeline.
- `src/preprocess_data.py`: Path-safe preprocessing script (one-hot encode categoricals, scale numerics, align features across subjects).
- `notebooks/`: EDA notebooks (`Main.ipynb`, `Analyze.ipynb`) with inline comments and auto plot-saving hooks.
- `Models/`: Model notebooks with detailed inline comments:
  - `Classification.ipynb`: Binary pass/fail classifiers (logistic regression, random forest, optional XGBoost), metrics, and plots.
  - `Regression.ipynb`: Grade prediction regressors (linear, random forest, optional XGBoost) with RMSE/R² comparisons.
  - `KMeans.ipynb`: Silhouette-driven K selection, PCA visualization, and cluster profiling.
- `scripts/plot_utils.py`: Notebook helper that auto-saves every open Matplotlib figure to `reports/plots/` at kernel exit (slugified filenames).
- `scripts/save_plots.py`: Batch executor that runs all notebooks and saves every figure to `reports/plots/` (uses lightweight seaborn shims if the library is missing).
- `scripts/student_merge.R`: Raw data merge helper for cross-subject analysis.
- `reports/plots/`: Generated figures (silhouette curves, PCA, confusion matrices, regression diagnostics) and Matplotlib cache.
- `docs/`: Project PDFs/notes.

## Dataset
- Source: UCI Machine Learning Repository – Student Performance (Math and Portuguese) datasets.
- Files: `student-mat.csv`, `student-por.csv` under `data/raw/` (semicolon-separated).
- Metadata: `student.txt` in `data/raw/` documents column definitions.

## Data & Preprocessing
1. Raw data already lives in `data/raw/`. If you refresh it, keep the same filenames.
2. Generate processed feature matrices:
   ```bash
   python -m src.preprocess_data
   ```
   Outputs: `data/processed/processed_mat.csv` and `data/processed/processed_por.csv`.
3. Downstream notebooks in `notebooks/` and `Models/` read from `data/raw/` or `data/processed/` (paths are relative and already updated).

## Plot Capture Workflow
- **Interactive notebooks:** Import `save_all_figs` from `scripts.plot_utils`; figures are auto-saved to `reports/plots/` when the kernel ends. You can also call `save_all_figs("title")` manually to snapshot current figures.
- **Batch export:** From the repo root, run:
  ```bash
  python scripts/save_plots.py
  ```
  This executes notebooks and saves every plot as PNGs under `reports/plots/`.

## Modeling Notebooks (high level)
- `Main.ipynb`: Quick EDA, outlier checks, and boxplots for math/Portuguese datasets.
- `Analyze.ipynb`: Distribution grids, full correlation heatmaps, G3 correlation tables, and KDE comparisons of key features across subjects.
- `Models/Classification.ipynb`: Trains/evaluates classifiers, saves confusion/ROC/PR plots, and writes summary CSVs.
- `Models/Regression.ipynb`: Trains regressors with/without G1/G2, compares RMSE/R², and saves residual/fit plots and summaries.
- `Models/KMeans.ipynb`: Tunes K via silhouette, visualizes clusters with PCA, and reports cluster feature means and pass rates.

## Outputs
- Processed data: `data/processed/processed_mat.csv`, `data/processed/processed_por.csv`.
- Plots: `reports/plots/` (EDA, classification, regression, clustering); additional run-specific subfolders may be created by notebooks (e.g., `plots_clustering`, `plots_classification`).
- Summaries: CSV exports from modeling notebooks (e.g., classification/regression summaries, cluster feature means/pass rates).

## Environment Notes
- Python 3.10+ recommended. Core deps: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn` (optional XGBoost if you enable those models).
- If you cannot install seaborn, `scripts/save_plots.py` includes minimal shims so batch plot export still works.
- Keep raw data intact; processed outputs live separately under `data/processed/`.

## Setup (recommended)
```bash
# create virtualenv (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# install core deps
pip install pandas numpy scikit-learn matplotlib seaborn

# optional: XGBoost for boosted models
pip install xgboost  # if available in your environment
```

## Quickstart
```bash
# 1) Preprocess data
python -m src.preprocess_data

# 2) Explore or model via notebooks (run in order; plots are auto-saved)
# 3) Batch-export plots without opening notebooks
python scripts/save_plots.py

# (Optional) Merge math/Portuguese records in R
Rscript scripts/student_merge.R
```

## Notes & Tips
- Notebook paths are relative to their folders; run them from within the repo root or the notebook directory to avoid path issues.
- `scripts/save_plots.py` uses a lightweight notebook executor and seaborn shims so figures are saved even without full plotting dependencies installed.
- Auto plot saving: importing `save_all_figs` from `scripts.plot_utils` will save all open Matplotlib figures to `reports/plots/` when the kernel exits; call `save_all_figs("title")` anytime to force a snapshot.
