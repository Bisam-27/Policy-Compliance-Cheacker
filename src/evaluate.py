import json
import os
from compliance_checker import ComplianceChecker
from pdf_processor import PDFProcessor
from config import RESULTS_FILE

def run_evaluation():
    """Evaluate the compliance checking system"""
    print("=" * 50)
    print("POLICY COMPLIANCE CHECKER EVALUATION")
    print("=" * 50)
    
    # Initialize system
    print("\n1. Initializing system...")
    try:
        checker = ComplianceChecker()
        print("✓ Compliance checker initialized")
        
        processor = PDFProcessor()
        processor.load_vector_store()
        print("✓ PDF processor and vector store loaded")
        
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        return
    
    # Test document search
    print("\n2. Testing document search functionality...")
    test_queries = [
        "password security requirements",
        "employee training mandatory",
        "data encryption standards",
        "access control procedures",
        "backup and recovery"
    ]
    
    search_results = {}
    for query in test_queries:
        try:
            results = processor.search_documents(query, k=3)
            search_results[query] = len(results)
            print(f"✓ '{query}': {len(results)} relevant documents found")
        except Exception as e:
            print(f"❌ '{query}': Error - {e}")
            search_results[query] = 0
    
    # Run compliance check
    print("\n3. Running full compliance analysis...")
    try:
        results = checker.run_full_compliance_check()
        print("✓ Compliance check completed successfully")
        
        # Display summary
        summary = results['summary']
        total = results['total_rules']
        
        print(f"\n✓ Total rules analyzed: {total}")
        print(f"✓ Compliant rules: {summary['compliant']} ({summary['compliant']/total*100:.1f}%)")
        print(f"✓ Partial compliance: {summary['partial']} ({summary['partial']/total*100:.1f}%)")
        print(f"✓ Non-compliant rules: {summary['non_compliant']} ({summary['non_compliant']/total*100:.1f}%)")
        print(f"✓ Not addressed: {summary['not_addressed']} ({summary['not_addressed']/total*100:.1f}%)")
        
        compliance_score = (summary['compliant'] + summary['partial']*0.5)/total*100
        print(f"\n✓ Overall compliance score: {compliance_score:.1f}%")
        
    except Exception as e:
        print(f"❌ Error during compliance check: {e}")
        return
    
    # Test specific rule analysis
    print("\n4. Testing individual rule analysis...")
    test_rules = ['data_protection', 'password_policy', 'employee_training']
    
    for rule_id in test_rules:
        if rule_id in results['rule_results']:
            rule_result = results['rule_results'][rule_id]
            status = rule_result['compliance_status']
            confidence = rule_result['confidence']
            evidence_count = len(rule_result['evidence'])
            
            print(f"✓ {rule_result['rule_title']}: {status} (confidence: {confidence:.2f}, evidence: {evidence_count} items)")
    
    # Generate detailed evaluation report
    print("\n5. Generating evaluation report...")
    
    evaluation_report = {
        'evaluation_timestamp': results['timestamp'],
        'system_performance': {
            'document_search_success_rate': sum(1 for count in search_results.values() if count > 0) / len(search_results),
            'total_documents_processed': len(set(meta['filename'] for meta in processor.chunk_metadata)),
            'total_chunks_created': len(processor.document_chunks),
            'compliance_rules_processed': total,
            'successful_rule_analyses': sum(1 for result in results['rule_results'].values() 
                                          if result['compliance_status'] != 'ERROR')
        },
        'compliance_metrics': {
            'overall_compliance_score': compliance_score,
            'compliant_percentage': summary['compliant']/total*100,
            'partial_compliance_percentage': summary['partial']/total*100,
            'non_compliant_percentage': summary['non_compliant']/total*100,
            'not_addressed_percentage': summary['not_addressed']/total*100
        },
        'search_test_results': search_results,
        'recommendations': generate_recommendations(results)
    }
    
    # Save evaluation report
    eval_file = os.path.join('data', 'evaluation_report.json')
    with open(eval_file, 'w') as f:
        json.dump(evaluation_report, f, indent=2)
    
    print(f"✓ Evaluation report saved to: {eval_file}")
    
    # Print final assessment
    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)
    
    performance = evaluation_report['system_performance']
    print(f"Documents processed: {performance['total_documents_processed']}")
    print(f"Text chunks created: {performance['total_chunks_created']}")
    print(f"Search success rate: {performance['document_search_success_rate']*100:.1f}%")
    print(f"Rules analyzed: {performance['compliance_rules_processed']}")
    print(f"Successful analyses: {performance['successful_rule_analyses']}")
    print(f"Overall compliance score: {compliance_score:.1f}%")
    
    if compliance_score >= 80:
        print("\n✅ EXCELLENT: High compliance achieved")
    elif compliance_score >= 60:
        print("\n⚠️ GOOD: Moderate compliance, some improvements needed")
    elif compliance_score >= 40:
        print("\n🟡 FAIR: Low compliance, significant improvements required")
    else:
        print("\n❌ POOR: Critical compliance issues need immediate attention")
    
    return evaluation_report

def generate_recommendations(results):
    """Generate recommendations based on compliance results"""
    recommendations = []
    
    summary = results['summary']
    total = results['total_rules']
    
    if summary['non_compliant'] > 0:
        recommendations.append(f"Address {summary['non_compliant']} non-compliant rules immediately")
    
    if summary['not_addressed'] > 0:
        recommendations.append(f"Create policies for {summary['not_addressed']} unaddressed compliance areas")
    
    if summary['partial'] > 0:
        recommendations.append(f"Enhance {summary['partial']} partially compliant policies")
    
    # Specific recommendations based on rule results
    critical_rules = ['data_protection', 'password_policy', 'access_control']
    
    for rule_id in critical_rules:
        if rule_id in results['rule_results']:
            rule_result = results['rule_results'][rule_id]
            if rule_result['compliance_status'] in ['NON_COMPLIANT', 'NOT_ADDRESSED']:
                recommendations.append(f"Priority: Address {rule_result['rule_title']} compliance")
    
    if not recommendations:
        recommendations.append("Maintain current compliance standards and conduct regular reviews")
    
    return recommendations

if __name__ == "__main__":
    evaluation_report = run_evaluation()
    print("\nEvaluation completed successfully!")