import os
import streamlit as st

# Configuration for Policy Compliance Checker
GEMINI_API_KEY = "AIzaSyAZDBX3kN86jDPUzRlHmGEkotE8_DT11Ok"

# Try to get from environment or Streamlit secrets
if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    except:
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# File paths
DATA_DIR = "data"
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
VECTOR_STORE_DIR = os.path.join(DATA_DIR, "vector_store")
RULES_FILE = os.path.join(DATA_DIR, "compliance_rules.json")
RESULTS_FILE = os.path.join(DATA_DIR, "compliance_results.json")

# Model settings
MODEL_NAME = "gemini-2.5-flash"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Create directories if they don't exist
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)