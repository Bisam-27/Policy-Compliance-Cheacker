import streamlit as st
import json
import os
from compliance_checker import ComplianceChecker
from pdf_processor import PDFProcessor
from compliance_rules import get_all_rules
from config import RESULTS_FILE

# Page configuration
st.set_page_config(
    page_title="Policy Compliance Checker",
    page_icon="📋",
    layout="wide"
)

def initialize_system():
    """Initialize the compliance checking system"""
    try:
        with st.spinner("Initializing compliance checking system..."):
            # Initialize PDF processor
            processor = PDFProcessor()
            
            # Check if we have documents and vector store
            if not os.path.exists("data/pdfs") or not os.listdir("data/pdfs"):
                st.info("No contract documents found. Creating CUAD contract documents...")
                processor.download_cuad_contracts()
            
            # Load or create vector store
            processor.load_vector_store()
            
            # Initialize compliance checker
            checker = ComplianceChecker()
            
            st.success("System initialized successfully!")
            return checker
            
    except Exception as e:
        st.error(f"Failed to initialize system: {e}")
        return None

def main():
    st.title("📋 Legal Contract Compliance Checker")
    st.markdown("""
    This system analyzes legal contracts from the CUAD dataset against predefined compliance rules 
    using AI-powered document retrieval and analysis.
    """)
    
    # Initialize system
    checker = initialize_system()
    if checker is None:
        st.stop()
    
    # Sidebar with system info
    with st.sidebar:
        st.header("System Information")
        
        # Show compliance rules
        rules = get_all_rules()
        st.write(f"**Total Compliance Rules:** {len(rules)}")
        
        # Show document info
        if os.path.exists("data/pdfs"):
            pdf_files = [f for f in os.listdir("data/pdfs") if f.endswith(('.txt', '.pdf'))]
            st.write(f"**Contract Documents:** {len(pdf_files)}")
            
            with st.expander("Document List"):
                for file in pdf_files:
                    st.write(f"• {file}")
        
        st.markdown("---")
        st.markdown("**Powered by Gemini AI**")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Run Compliance Check", "View Results", "Rule Details", "Document Search"])
    
    with tab1:
        st.header("🔍 Run Compliance Check")
        st.write("Analyze all legal contracts against compliance rules.")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("Start Compliance Check", type="primary"):
                with st.spinner("Running compliance analysis..."):
                    try:
                        results = checker.run_full_compliance_check()
                        st.success("Compliance check completed!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error during compliance check: {e}")
        
        with col2:
            if os.path.exists(RESULTS_FILE):
                st.info("Previous compliance results found. Click 'View Results' tab to see them.")
    
    with tab2:
        st.header("📊 Compliance Results")
        
        if os.path.exists(RESULTS_FILE):
            try:
                with open(RESULTS_FILE, 'r') as f:
                    results = json.load(f)
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                summary = results['summary']
                total = results['total_rules']
                
                with col1:
                    st.metric("✅ Compliant", summary['compliant'], f"{summary['compliant']/total*100:.1f}%")
                with col2:
                    st.metric("⚠️ Partial", summary['partial'], f"{summary['partial']/total*100:.1f}%")
                with col3:
                    st.metric("❌ Non-Compliant", summary['non_compliant'], f"{summary['non_compliant']/total*100:.1f}%")
                with col4:
                    compliance_score = (summary['compliant'] + summary['partial']*0.5)/total*100
                    st.metric("Overall Score", f"{compliance_score:.1f}%")
                
                st.markdown("---")
                
                # Detailed results
                st.subheader("Detailed Rule Analysis")
                
                for rule_id, rule_result in results['rule_results'].items():
                    status = rule_result['compliance_status']
                    
                    # Status emoji mapping
                    status_emojis = {
                        'COMPLIANT': '✅',
                        'PARTIAL': '⚠️',
                        'NON_COMPLIANT': '❌',
                        'NOT_ADDRESSED': '❓',
                        'ERROR': '⚠️'
                    }
                    
                    with st.expander(f"{status_emojis.get(status, '❓')} {rule_result['rule_title']} - {status}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**Confidence:** {rule_result['confidence']:.2f}")
                            
                            if rule_result['evidence']:
                                st.write("**Evidence Found:**")
                                for evidence in rule_result['evidence']:
                                    st.write(f"• {evidence}")
                            
                            if rule_result['suggestions']:
                                st.write("**Suggestions:**")
                                for suggestion in rule_result['suggestions']:
                                    st.write(f"• {suggestion}")
                        
                        with col2:
                            if rule_result['retrieved_content']:
                                st.write("**Source Documents:**")
                                for content in rule_result['retrieved_content']:
                                    st.write(f"📄 {content['source']} (Score: {content['similarity']:.3f})")
                                    with st.expander("Preview"):
                                        st.write(content['content'])
                
            except Exception as e:
                st.error(f"Error loading results: {e}")
        else:
            st.info("No compliance results found. Please run a compliance check first.")
    
    with tab3:
        st.header("📝 Compliance Rules")
        st.write("Overview of all compliance rules used in the analysis.")
        
        rules = get_all_rules()
        
        for rule_id, rule_data in rules.items():
            with st.expander(f"🔍 {rule_data['title']}"):
                st.write(f"**Description:** {rule_data['description']}")
                st.write(f"**Keywords:** {', '.join(rule_data['keywords'])}")
    
    with tab4:
        st.header("🔎 Document Search")
        st.write("Search through contract documents to find specific clauses and provisions.")
        
        search_query = st.text_input("Enter search query:", placeholder="e.g., liability limitation, termination clause, confidentiality")
        
        if search_query:
            with st.spinner("Searching documents..."):
                try:
                    processor = PDFProcessor()
                    processor.load_vector_store()
                    results = processor.search_documents(search_query, k=5)
                    
                    if results:
                        st.write(f"Found {len(results)} relevant sections:")
                        
                        for i, result in enumerate(results, 1):
                            with st.expander(f"Result {i}: {result['metadata']['filename']} (Score: {result['similarity']:.3f})"):
                                st.write(result['content'])
                                st.caption(f"Source: {result['metadata']['filename']}, Chunk {result['metadata']['chunk_id']+1}/{result['metadata']['total_chunks']}")
                    else:
                        st.info("No relevant documents found for your query.")
                        
                except Exception as e:
                    st.error(f"Error searching documents: {e}")

if __name__ == "__main__":
    main()