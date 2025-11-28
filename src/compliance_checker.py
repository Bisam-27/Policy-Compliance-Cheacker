import json
import os
from typing import List, Dict, Any
import google.generativeai as genai
from pdf_processor import PDFProcessor
from compliance_rules import get_all_rules, get_rule
from config import GEMINI_API_KEY, MODEL_NAME, RESULTS_FILE

class ComplianceChecker:
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(MODEL_NAME)
        
        # Initialize PDF processor
        self.pdf_processor = PDFProcessor()
        self.pdf_processor.load_vector_store()
        
        # Load compliance rules
        self.rules = get_all_rules()
        
    def check_rule_compliance(self, rule_id: str, rule_data: Dict) -> Dict[str, Any]:
        """Check compliance for a specific rule"""
        # Search for relevant documents
        search_query = f"{rule_data['title']} {' '.join(rule_data['keywords'])}"
        relevant_docs = self.pdf_processor.search_documents(search_query, k=3)
        
        if not relevant_docs:
            return {
                'rule_id': rule_id,
                'rule_title': rule_data['title'],
                'compliance_status': 'NOT_FOUND',
                'confidence': 0.0,
                'evidence': [],
                'suggestions': ['No relevant policy documents found for this rule'],
                'retrieved_content': []
            }
        
        # Prepare context for Gemini
        context = "\n\n".join([doc['content'] for doc in relevant_docs])
        
        # Create compliance checking prompt
        prompt = f"""
You are a compliance expert analyzing company policy documents. 

Rule to Check:
Title: {rule_data['title']}
Description: {rule_data['description']}
Keywords: {', '.join(rule_data['keywords'])}

Policy Documents Context:
{context}

Analyze whether the policy documents comply with this rule. Provide:
1. Compliance status (COMPLIANT, PARTIAL, NON_COMPLIANT, or NOT_ADDRESSED)
2. Confidence score (0.0 to 1.0)
3. Specific evidence from the documents (quote relevant sections)
4. Suggestions for improvement if non-compliant

Respond in this exact JSON format:
{{
    "compliance_status": "COMPLIANT/PARTIAL/NON_COMPLIANT/NOT_ADDRESSED",
    "confidence": 0.0,
    "evidence": ["quote1", "quote2"],
    "suggestions": ["suggestion1", "suggestion2"]
}}
"""
        
        try:
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Try to extract JSON from response
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_text = response_text[json_start:json_end]
            elif '{' in response_text and '}' in response_text:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                json_text = response_text[json_start:json_end]
            else:
                json_text = response_text
            
            # Parse the JSON response
            analysis = json.loads(json_text)
            
            # Add additional metadata
            analysis.update({
                'rule_id': rule_id,
                'rule_title': rule_data['title'],
                'retrieved_content': [{
                    'content': doc['content'][:200] + '...' if len(doc['content']) > 200 else doc['content'],
                    'source': doc['metadata']['filename'],
                    'similarity': doc['similarity']
                } for doc in relevant_docs]
            })
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing rule {rule_id}: {e}")
            return {
                'rule_id': rule_id,
                'rule_title': rule_data['title'],
                'compliance_status': 'ERROR',
                'confidence': 0.0,
                'evidence': [],
                'suggestions': [f'Error occurred during analysis: {str(e)}'],
                'retrieved_content': []
            }
    
    def run_full_compliance_check(self) -> Dict[str, Any]:
        """Run compliance check for all rules"""
        results = {
            'timestamp': None,
            'total_rules': len(self.rules),
            'rule_results': {},
            'summary': {
                'compliant': 0,
                'partial': 0,
                'non_compliant': 0,
                'not_addressed': 0,
                'errors': 0
            }
        }
        
        print(f"Starting compliance check for {len(self.rules)} rules...")
        
        for rule_id, rule_data in self.rules.items():
            print(f"Checking rule: {rule_data['title']}")
            
            rule_result = self.check_rule_compliance(rule_id, rule_data)
            results['rule_results'][rule_id] = rule_result
            
            # Update summary
            status = rule_result['compliance_status'].upper()
            if status == 'COMPLIANT':
                results['summary']['compliant'] += 1
            elif status == 'PARTIAL':
                results['summary']['partial'] += 1
            elif status == 'NON_COMPLIANT':
                results['summary']['non_compliant'] += 1
            elif status == 'NOT_ADDRESSED':
                results['summary']['not_addressed'] += 1
            else:
                results['summary']['errors'] += 1
        
        # Add timestamp
        from datetime import datetime
        results['timestamp'] = datetime.now().isoformat()
        
        # Save results
        os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
        with open(RESULTS_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nCompliance check complete!")
        print(f"Results saved to: {RESULTS_FILE}")
        
        return results
    
    def get_compliance_summary(self) -> str:
        """Generate a human-readable compliance summary"""
        try:
            with open(RESULTS_FILE, 'r') as f:
                results = json.load(f)
        except FileNotFoundError:
            return "No compliance results found. Please run a compliance check first."
        
        summary = results['summary']
        total = results['total_rules']
        
        summary_text = f"""
COMPLIANCE SUMMARY
==================

Total Rules Checked: {total}

✅ Compliant: {summary['compliant']} ({summary['compliant']/total*100:.1f}%)
⚠️  Partial: {summary['partial']} ({summary['partial']/total*100:.1f}%)
❌ Non-Compliant: {summary['non_compliant']} ({summary['non_compliant']/total*100:.1f}%)
❓ Not Addressed: {summary['not_addressed']} ({summary['not_addressed']/total*100:.1f}%)

Overall Compliance Score: {(summary['compliant'] + summary['partial']*0.5)/total*100:.1f}%
"""
        return summary_text
    
    def get_detailed_results(self) -> Dict:
        """Load and return detailed compliance results"""
        try:
            with open(RESULTS_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

if __name__ == "__main__":
    checker = ComplianceChecker()
    results = checker.run_full_compliance_check()
    print(checker.get_compliance_summary())