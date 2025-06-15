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
├── .secrets/          # Service account JSON for GDrive DVC push
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
  * Developed and committed a full EDA notebook (`notebooks/eda_task1.ipynb`) with annotated insights and visualizations

*  **Task 2**:

  * Installed and configured DVC with Google Drive remote
  * Added raw dataset using `dvc add` and committed pointer files
  * Configured `gdrive_remote` with service account from `.secrets/`
  * Successfully pushed data using secure authentication
  * Updated `.gitignore` to exclude secrets and DVC cache

*  **Task 3** (Upcoming): A/B Hypothesis Testing

---

##  Data Version Control (DVC)

* Initialized DVC in the project using `dvc init`
* Configured remote: `dvc remote add -d gdrive_remote gdrive://<folder_id>`
* Used service account for auth: `.secrets/gdrive-service-account.json`
* Added raw dataset: `data/raw/MachineLearningRating_v3.txt` with `dvc add`
* Committed DVC files to Git and pushed data using `dvc push`

---

##  Testing

Run all tests:

```bash
pytest
```

---

## CI/CD

GitHub Actions runs automated tests on every push and pull request.
Workflow file: `.github/workflows/Project.yml`

---

##  Author

Hiwot ([@lhiwi](https://github.com/lhiwi))
10 Academy AI Mastery Program
