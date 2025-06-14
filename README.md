# ACIS Insurance Risk Analytics

End-to-end insurance analytics project for AlphaCare Insurance Solutions (ACIS).

This project analyzes historical auto insurance data to identify low-risk segments and optimize premiums using machine learning.

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

## 📁 Structure

```
├── src/               # Core modules
├── scripts/           # Entry-point scripts
├── notebooks/         # Jupyter notebooks for analysis
├── tests/             # Pytest unit tests
├── data/raw/          # Input data (not tracked by Git)
├── .github/workflows/ # CI/CD configs
├── .vscode/           # VS Code settings
├── .gitignore         
├── README.md          
├── requirements.txt   
```

---

## 🚀 Usage

Work inside branches:

```bash
git checkout -b task-1
```

Run notebooks via:

```bash
cd notebooks
jupyter notebook
```

---

## 🧪 Testing

Run all tests:

```bash
pytest
```
---

## 📌 Author

Hiwot ([@lhiwi](https://github.com/lhiwi))
10 Academy AI Mastery Program
