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

  * Set up GitHub repository and configured Git versioning
  * Created clean modular project structure and VS Code workspace
  * Activated virtual environment and added dependencies
  * Added CI/CD workflow with GitHub Actions
  * Performed comprehensive EDA:

    * Investigated distribution of `TotalClaims` and `TotalPremium`
    * Explored temporal trends by `TransactionMonth`
    * Analyzed correlation matrix of numeric features
    * Highlighted key drivers via scatter and line plots

*  **Task 2**:

  * Installed and initialized DVC
  * Tracked dataset with DVC using: `dvc add data/raw/MachineLearningRating_v3.txt`
  * Configured remote storage using Google Drive service account
  * Authenticated and pushed data using `dvc push`
  * Updated `.gitignore` to safely exclude large or sensitive data

*  **Task 3**: A/B Hypothesis Testing

  * Conducted statistical hypothesis testing on urban vs. rural segments
  * Analyzed premium margins and loss ratios by ZIP code
  * Calculated effect sizes and segment-specific risk performance

*  **Task 4**: Predictive Modeling and Premium Optimization

  * Preprocessed mixed data types (dates, categoricals, numericals)
  * Built classification model (XGBoost + SMOTE) to predict claim occurrence
  * Developed regression model (XGBoost) to predict claim severity
  * Applied SHAP for explainability and feature impact interpretation
  * Trained and evaluated models using metrics: RMSE, R-squared, precision, recall
  * Saved trained models and preprocessing pipeline using joblib

---

##  Data Version Control (DVC)

* DVC initialized via `dvc init`
* Remote configured using Google Drive with service account authentication
* Secrets securely stored in `.secrets/`
* DVC metadata committed to Git (excluding large files)

---

##  Testing

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
