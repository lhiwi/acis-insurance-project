import streamlit as st
import pandas as pd
import numpy as np
import joblib
from scipy import sparse
import shap
import os
import re
from io import BytesIO

# Configuration
MODEL_DIR = r"C:\Users\jilow\OneDrive\Documents\acis-insurance-project\models"
REQUIRED_COLUMNS = [
    'TransactionMonth', 'PostalCode', 'RegistrationYear', 'VehicleType',
    'SumInsured', 'CalculatedPremiumPerTerm', 'Province', 'make', 'Model'
]

# Construct full paths to model files
CLF_MODEL_PATH = os.path.join(MODEL_DIR, "claim_occurrence_model.pkl")
REG_MODEL_PATH = os.path.join(MODEL_DIR, "claim_severity_model.pkl")
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, "preprocessor.pkl")

# Load resources with error handling
@st.cache_resource(show_spinner="Loading risk models...")
def load_resources():
    try:
        # Verify files exist before loading
        if not all(os.path.exists(p) for p in [CLF_MODEL_PATH, REG_MODEL_PATH, PREPROCESSOR_PATH]):
            missing = [p for p in [CLF_MODEL_PATH, REG_MODEL_PATH, PREPROCESSOR_PATH] if not os.path.exists(p)]
            st.error(f"Model files missing: {', '.join(missing)}")
            st.stop()
            
        clf_model = joblib.load(CLF_MODEL_PATH)
        reg_model = joblib.load(REG_MODEL_PATH)
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        return clf_model, reg_model, preprocessor
    except Exception as e:
        st.error(f"Model loading failed: {str(e)}")
        st.stop()

# Detect delimiter for text files
def detect_delimiter(file_path, sample_size=1024):
    with open(file_path, 'r') as f:
        sample = f.read(sample_size)
    
    # Check for common delimiters
    for delim in [',', ';', '\t', '|']:
        if sample.count(delim) > sample.count('\n'):
            return delim
    
    # Try regex for space-separated
    if re.search(r'\s{2,}', sample):
        return r'\s+'
    
    # Default to comma if nothing found
    return ','

# Universal file loader
def load_any_file(uploaded_file):
    file_name = uploaded_file.name.lower()
    file_extension = os.path.splitext(file_name)[1]
    
    try:
        # Handle CSV and TXT files
        if file_extension in ['.csv', '.txt']:
            # Save to temp file for delimiter detection
            temp_path = f"temp{file_extension}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Detect delimiter and encoding
            delim = detect_delimiter(temp_path)
            encoding = 'utf-8'
            
            # Try reading with detected delimiter
            try:
                return pd.read_csv(temp_path, delimiter=delim, encoding=encoding)
            except:
                # Try different encodings if needed
                for enc in ['latin1', 'ISO-8859-1', 'cp1252']:
                    try:
                        return pd.read_csv(temp_path, delimiter=delim, encoding=enc)
                    except:
                        pass
            
            # Fallback to read with error handling
            return pd.read_csv(temp_path, delimiter=None, engine='python', encoding=encoding)
        
        # Handle Excel files
        elif file_extension in ['.xlsx', '.xls']:
            return pd.read_excel(uploaded_file, engine='openpyxl')
        
        # Handle JSON files
        elif file_extension == '.json':
            return pd.read_json(uploaded_file)
        
        # Handle Parquet files
        elif file_extension == '.parquet':
            return pd.read_parquet(uploaded_file)
        
        # Handle other formats
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None
            
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

# Initialize app
st.set_page_config(
    page_title="ACIS Insurance Risk Pricing Engine",
    page_icon="📊",
    layout="wide"
)

# Header with warning banner
st.markdown(
    """
    <div style='background-color: #ffcccc; padding: 10px; border-radius: 5px;'>
    <h3 style='color: #cc0000;'>VALIDATION MODE - NOT FOR PRODUCTION USE</h3>
    <p>Current model limitations: Claim detection rate 18% (target >65%), 
    Severity prediction error ±$37,878 (target <$10,000)</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("ACIS Risk-Based Insurance Pricing")
st.subheader("Universal Policy Data Processor")

# Sidebar configuration
st.sidebar.header("Configuration")
st.sidebar.write(f"Model directory: {MODEL_DIR}")
validation_mode = st.sidebar.checkbox("Enable validation safeguards", True)
show_explanations = st.sidebar.checkbox("Show risk explanations", True)
deployment_mode = st.sidebar.selectbox(
    "Environment", 
    ["Validation", "Staging", "Production"], 
    index=0
)

# Load models
clf_model, reg_model, preprocessor = load_resources()
st.sidebar.success("Models loaded successfully!")

# Supported file types
supported_types = ["csv", "txt", "xlsx", "xls", "json", "parquet"]

# File upload section
uploaded_file = st.file_uploader(
    "Upload policy data", 
    type=supported_types,
    help=f"Supported formats: {', '.join(supported_types)}"
)

if uploaded_file:
    try:
        # Read file using universal loader
        with st.spinner(f"Reading {uploaded_file.name}..."):
            data = load_any_file(uploaded_file)
            
        if data is None:
            st.error("Failed to process uploaded file")
            st.stop()
            
        # Show data preview
        st.subheader("Raw Data Preview")
        st.write(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")
        st.dataframe(data.head(3))
        
        # Convert column names to match expected format
        data.columns = data.columns.str.strip().str.replace(' ', '')
        
        # Validation checks
        missing_cols = set(REQUIRED_COLUMNS) - set(data.columns)
        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
            st.info("Available columns: " + ", ".join(data.columns))
            st.stop()
            
        if validation_mode and len(data) > 5000:
            st.warning("Large dataset detected. Sampling first 5,000 records.")
            data = data.head(5000)
            
        # Preprocessing
        with st.spinner("Preprocessing data..."):
            X_raw = data.copy()
            X_processed = preprocessor.transform(data)
            X_dense = X_processed.toarray() if sparse.issparse(X_processed) else X_processed
        
        # Predictions
        with st.spinner("Calculating risks..."):
            # Claim probability
            claim_probs = clf_model.predict_proba(X_dense)[:, 1]
            
            # Adjusted threshold based on deployment mode
            threshold = 0.3 if deployment_mode == "Validation" else 0.5
            predicted_claim = (claim_probs > threshold).astype(int)
            
            # Claim severity
            severity_preds = reg_model.predict(X_dense)
            
            # Premium calculation with safety margins
            base_premium = claim_probs * severity_preds
            risk_load = np.where(claim_probs > 0.4, 0.35, 0.15)
            uncertainty_multiplier = 1 + (0.5 - clf_model.predict_proba(X_dense)[:, 0])
            recommended_premium = base_premium * (1.2 + risk_load) * uncertainty_multiplier
            
            # Apply environment multiplier
            if deployment_mode == "Production":
                recommended_premium *= 1.3
            elif deployment_mode == "Staging":
                recommended_premium *= 1.1
                
        # Prepare results
        results = data.copy()
        results["Risk_Score"] = claim_probs
        results["Predicted_Claim"] = predicted_claim
        results["Expected_Severity"] = severity_preds
        results["Recommended_Premium"] = recommended_premium
        
        # Display results
        st.success(f"Processed {len(results)} policies")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("High-Risk Policies", 
                      f"{results[results['Risk_Score'] > 0.7].shape[0]}",
                      "Require manual review")
        
        with col2:
            if 'CalculatedPremiumPerTerm' in results:
                avg_premium_diff = np.mean(
                    results["Recommended_Premium"] - results["CalculatedPremiumPerTerm"]
                )
                st.metric("Avg. Premium Adjustment", 
                          f"${avg_premium_diff:,.2f}", 
                          "vs current pricing")
            else:
                st.metric("Avg. Recommended Premium", 
                          f"${results['Recommended_Premium'].mean():,.2f}")
        
        # Interactive results table
        st.subheader("Policy Risk Assessment")
        display_cols = ['Risk_Score', 'Predicted_Claim', 'Expected_Severity', 'Recommended_Premium']
        display_cols = [c for c in display_cols if c in results.columns]
        
        st.dataframe(
            results[display_cols].head(20).style.format({
                'Risk_Score': '{:.2%}',
                'Expected_Severity': '${:,.2f}',
                'Recommended_Premium': '${:,.2f}'
            }),
            height=400
        )
        
        # Risk explanations
        if show_explanations:
            st.subheader("Risk Explanation for First Policy")
            sample_idx = 0
            
            # SHAP explanation
            explainer = shap.TreeExplainer(clf_model)
            shap_values = explainer.shap_values(X_dense[sample_idx])
            
            # Get feature names
            try:
                feature_names = preprocessor.get_feature_names_out()
            except:
                feature_names = [f"Feature_{i}" for i in range(X_dense.shape[1])]
            
            # Display force plot
            st_shap(shap.force_plot(
                explainer.expected_value,
                shap_values,
                X_dense[sample_idx],
                feature_names=feature_names
            ))
            
            # Top risk factors
            st.write("Top risk contributors:")
            shap_df = pd.DataFrame({
                'Feature': feature_names,
                'Impact': shap_values
            }).sort_values('Impact', ascending=False, key=abs).head(10)
            st.dataframe(shap_df)
        
        # Download options
        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Full Results", 
            data=csv, 
            file_name="acis_risk_assessment.csv", 
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Processing failed: {str(e)}")
        st.stop()

else:
    st.info("Upload a data file to begin risk assessment")
    st.markdown("""
    **Supported file formats:**
    - CSV (.csv)
    - Text files (.txt) with any delimiter
    - Excel (.xlsx, .xls)
    - JSON (.json)
    - Parquet (.parquet)
    
    **Required columns must include:**
    - TransactionMonth, PostalCode, RegistrationYear
    - VehicleType, SumInsured, CalculatedPremiumPerTerm
    - Province, make, Model
    """)

# SHAP rendering function
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    st.components.v1.html(shap_html, height=height)