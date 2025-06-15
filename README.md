# ACIS Insurance Risk Analytics

End-to-end insurance analytics project for AlphaCare Insurance Solutions (ACIS).

This project analyzes historical auto insurance data to identify low-risk segments and optimize premiums using machine learning. It includes data versioning, testing, CI/CD automation, and reproducible pipelines.

---

## 🔧 Setup

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

*  Task 1: Git setup, project scaffold, EDA notebook (`eda_task1.ipynb`)
*  Task 2: Initialized DVC, configured local remote, tracked dataset
*  Task 3: A/B Hypothesis Testing (next)

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
