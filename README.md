# ACIS Insurance Risk Analytics

End-to-end insurance analytics project for AlphaCare Insurance Solutions (ACIS).

This project analyzes historical auto insurance data to identify low-risk segments and optimize premiums using machine learning. It includes data versioning, testing, CI/CD automation, and reproducible pipelines.

---

##  Setup

```bash
# Clone repo
https://github.com/lhiwi/acis-insurance-project.git
cd acis-insurance-project

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

##  Structure

```
├── src/               # Core modules (__init__.py, utils.py, etc.)
├── scripts/           # Entry-point scripts
├── notebooks/         # Jupyter notebooks for EDA and modeling
├── tests/             # Pytest unit tests (e.g. test_dummy.py)
├── data/raw/          # Input data (versioned with DVC)
├── dvcstore/          # Local DVC remote storage
├── .github/workflows/ # CI/CD GitHub Actions
├── .vscode/           # VS Code settings
├── .dvc/              # DVC config and state
├── .gitignore         # Git ignore file
├── requirements.txt   # Project dependencies
├── README.md          # Project overview
```

---

##  Progress

*  **Task 1**:

  * Set up GitHub repository and linked remote origin
  * Created clean project folder structure with modular components
  * Configured virtual environment and added core dependencies
  * Added VS Code settings and GitHub Actions for CI/CD
  * Developed and committed a full EDA notebook (`notebooks/eda_task1.ipynb`) with exploratory insights and visualizations

*  **Task 2**:

  * Installed and configured DVC
  * Added raw dataset using `dvc add` and committed metadata files
  * Configured a local DVC remote (`dvcstore/`) and pushed data via `dvc push`
  * All data version control steps committed in `task-2` branch

* **Task 3** (Upcoming): A/B Hypothesis Testing

---

##  Data Version Control (DVC)

* Initialized DVC in the project using `dvc init`
* Configured local remote storage: `dvc remote add -d localstorage ./dvcstore`
* Added raw dataset: `data/raw/MachineLearningRating_v3.txt` with `dvc add`
* Committed DVC metadata files to Git (`.dvc/config`, `.gitignore`, `.dvc` directory)
* Used `dvc push` to store data in local remote directory for reproducibility

---

##  Testing

Run all tests:

```bash
pytest
```

---

##  CI/CD

GitHub Actions runs automated tests on every push and pull request.
Workflow file: `.github/workflows/Project.yml`

---

##  Author

Hiwot ([@lhiwi](https://github.com/lhiwi))
10 Academy AI Mastery Program
