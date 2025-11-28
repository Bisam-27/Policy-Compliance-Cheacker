# Policy Compliance Checker RAG System

A LangChain-based RAG system that evaluates legal contracts from the CUAD dataset against predefined compliance rules using Google Gemini AI.

## Features

- **15 Compliance Rules**: Comprehensive coverage of security, HR, and IT policies
- **PDF Document Processing**: Automatic ingestion and chunking of policy documents
- **AI-Powered Analysis**: Uses Google Gemini for intelligent compliance evaluation
- **Interactive Web Interface**: Streamlit-based demo for easy policy analysis
- **Detailed Reporting**: Comprehensive compliance reports with evidence and suggestions

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run src/app.py
   ```

3. **Use the System**
   - The app will create sample policy documents automatically
   - Click "Start Compliance Check" to analyze policies
   - View detailed results and recommendations

## System Architecture

- `src/config.py` - Configuration and API keys
- `src/compliance_rules.py` - 15 predefined compliance rules
- `src/pdf_processor.py` - Document processing and vector store
- `src/compliance_checker.py` - Main compliance analysis engine
- `src/app.py` - Streamlit web interface
- `src/evaluate.py` - System evaluation and testing

## Legal Compliance Rules Covered

1. Liability Limitation Clauses
2. Termination and Cure Period Rights
3. Confidentiality and Non-Disclosure Obligations
4. Intellectual Property Ownership
5. Payment Terms and Conditions
6. Data Protection and Privacy Laws Compliance
7. Service Level Agreements
8. Governing Law and Jurisdiction
9. Insurance and Coverage Requirements
10. Regulatory and Standards Compliance
11. Force Majeure Provisions
12. Assignment and Transfer Rights
13. Audit Rights and Reporting
14. Security Incident Notification
15. Survival of Contract Terms

## Usage

### Web Interface
1. **Run Compliance Check**: Analyze all policies against compliance rules
2. **View Results**: See detailed compliance status and recommendations
3. **Rule Details**: Explore individual compliance rules
4. **Document Search**: Search through policy documents

### Command Line
```bash
# Run evaluation
python src/evaluate.py

# Process documents
python src/pdf_processor.py

# Run compliance check
python src/compliance_checker.py
```

## Sample Output

The system provides:
- Compliance status for each rule (COMPLIANT/PARTIAL/NON_COMPLIANT/NOT_ADDRESSED)
- Confidence scores for analyses
- Specific evidence from policy documents
- Improvement suggestions for non-compliant areas
- Overall compliance score

## Technical Details

- **Vector Store**: TF-IDF based document similarity search
- **LLM**: Google Gemini 1.5 Flash model
- **Document Processing**: Text chunking with 1000 character chunks, 200 character overlap
- **Search**: Cosine similarity based retrieval

## Requirements

- Python 3.8+
- Google Gemini API key
- Streamlit
- scikit-learn
- numpy

This system demonstrates a practical application of RAG technology for regulatory compliance checking in enterprise environments.