import os
import json
import requests
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import numpy as np
from config import PDF_DIR, VECTOR_STORE_DIR, CHUNK_SIZE, CHUNK_OVERLAP

class PDFProcessor:
    def __init__(self):
        self.vectorizer = None
        self.document_chunks = []
        self.chunk_metadata = []
        
    def download_cuad_contracts(self):
        """Create sample legal contract documents based on CUAD dataset structure"""
        print("Creating CUAD-style contract documents for compliance checking...")
        
        # Legal contracts based on CUAD dataset structure
        cuad_contracts = {
            "software_license_agreement.txt": """
SOFTWARE LICENSE AGREEMENT

1. DEFINITIONS AND INTERPRETATIONS
"Agreement" means this Software License Agreement and all amendments hereto.
"Company" refers to TechCorp Solutions, Inc., the licensor of the software.
"Licensee" means the entity or individual acquiring rights under this Agreement.
"Software" includes the computer program, documentation, and related materials.
"Confidential Information" means all proprietary and non-public information.

2. GRANT OF LICENSE AND RESTRICTIONS
Company hereby grants Licensee a non-exclusive, non-transferable license to use the Software.
Licensee may install the Software on up to five (5) designated computer systems.
Licensee shall not reverse engineer, decompile, or create derivative works.
No sublicensing rights are granted without express written consent.

3. DATA PROTECTION AND PRIVACY COMPLIANCE
All personal data collected must be encrypted using AES-256 encryption standards.
Data processing activities shall comply with GDPR, CCPA, and applicable privacy regulations.
Personal information retention period limited to three (3) years post-termination.
Data subjects retain rights to access, rectification, and erasure of personal data.
Cross-border data transfers require adequate protection mechanisms.

4. SECURITY AND COMPLIANCE OBLIGATIONS  
Licensee must implement multi-factor authentication for all user accounts.
Security incident notifications required within twenty-four (24) hours.
Annual security assessments by certified third-party auditors mandatory.
Compliance with SOC 2 Type II and ISO 27001 standards required.

5. LIMITATION OF LIABILITY AND INDEMNIFICATION
Company's total liability limited to fees paid in the twelve (12) months preceding claim.
Neither party liable for indirect, incidental, or consequential damages.
Each party indemnifies the other against third-party intellectual property claims.
Liability limitations do not apply to data breaches or willful misconduct.

6. TERM AND TERMINATION
Initial term of three (3) years with automatic renewal unless terminated.
Either party may terminate for material breach with thirty (30) days cure period.
Immediate termination permitted for insolvency or violation of confidentiality.
Surviving provisions include confidentiality, liability limitations, and governing law.

7. GOVERNING LAW AND DISPUTE RESOLUTION
Agreement governed by laws of Delaware, excluding conflict of law principles.
Disputes resolved through binding arbitration under AAA Commercial Rules.
Arbitration conducted in Delaware with single arbitrator.
Equitable relief available for breach of confidentiality or intellectual property.
""",
            
            "service_provider_agreement.txt": """
PROFESSIONAL SERVICES AGREEMENT

1. SCOPE OF SERVICES AND DELIVERABLES
Provider shall deliver consulting services as specified in attached Statement of Work.
Services include business process analysis, system implementation, and staff training.
Project timeline spans twelve (12) months with defined milestones and deliverables.
Additional services require written authorization and separate pricing.

2. COMPENSATION AND PAYMENT TERMS
Total project fee of Two Hundred Thousand Dollars ($200,000) payable monthly.
Expenses reimbursed at cost with receipts and prior written approval.
Payment terms Net Thirty (30) days from receipt of undisputed invoice.
Late payments subject to interest at rate of one and one-half percent (1.5%) monthly.

3. CONFIDENTIALITY AND NON-DISCLOSURE
Both parties acknowledge receipt of confidential and proprietary information.
Confidential information includes business processes, customer data, and technical specifications.
Confidentiality obligations survive termination for period of five (5) years.
Disclosure permitted only to employees with legitimate business need-to-know.

4. PERSONNEL AND SECURITY REQUIREMENTS
All Provider personnel must complete background checks before client site access.
Security training certification required within first week of engagement.
Multi-factor authentication mandatory for all system access and data handling.
Provider personnel subject to client security policies and procedures.

5. INTELLECTUAL PROPERTY AND WORK PRODUCT
Client retains ownership of all work product and deliverables created hereunder.
Provider grants Client perpetual, royalty-free license to methodologies and tools.
Pre-existing Provider intellectual property remains Provider's exclusive property.
Client grants Provider limited license to use Client trademarks for marketing.

6. INSURANCE AND RISK MANAGEMENT
Provider maintains professional liability insurance minimum Five Million Dollars ($5,000,000).
General liability coverage minimum Two Million Dollars ($2,000,000) per occurrence.
Cyber liability insurance minimum Ten Million Dollars ($10,000,000) required.
Client named as additional insured on all applicable policies.

7. COMPLIANCE AND REGULATORY REQUIREMENTS
Provider must comply with all applicable federal, state, and local regulations.
HIPAA compliance required for access to protected health information.
SOX compliance mandatory for financial system access and data handling.
Regular compliance audits and certifications provided upon Client request.
""",
            
            "employment_agreement.txt": """
EXECUTIVE EMPLOYMENT AGREEMENT

1. POSITION AND RESPONSIBILITIES
Employee appointed as Chief Information Officer reporting to Chief Executive Officer.
Primary duties include technology strategy, IT operations, and digital transformation.
Authority to manage IT department budget and make technology investment decisions.
Expected to work full-time with occasional travel and extended hours as required.

2. COMPENSATION AND BENEFITS PACKAGE
Base salary of Three Hundred Thousand Dollars ($300,000) annually, paid bi-weekly.
Eligible for annual performance bonus up to fifty percent (50%) of base salary.
Equity compensation includes stock options for 0.5% of company shares.
Benefits include health, dental, vision insurance, and 401(k) with company matching.

3. CONFIDENTIALITY AND PROPRIETARY INFORMATION
Employee acknowledges access to confidential business information and trade secrets.
Confidential information includes customer lists, financial data, and strategic plans.
Non-disclosure obligations continue indefinitely after employment termination.
Return of all confidential information and company property upon separation.

4. NON-COMPETITION AND NON-SOLICITATION
Employee agrees not to compete with Company for two (2) years post-termination.
Geographic restriction applies to all locations where Company conducts business.
Non-solicitation of employees and customers for eighteen (18) months after separation.
Garden leave provisions may apply during notice period at Company discretion.

5. INTELLECTUAL PROPERTY ASSIGNMENT
All inventions and work product during employment assigned to Company.
Employee represents no conflicting obligations to former employers exist.
Company owns all patents, copyrights, and trade secrets developed using Company resources.
Pre-existing employee intellectual property specifically excluded from assignment.

6. TERMINATION AND SEVERANCE
Employment terminable by either party with sixty (60) days written notice.
Immediate termination for cause including misconduct, breach, or criminal activity.
Severance package includes twelve (12) months salary continuation for without-cause termination.
Accelerated vesting of equity compensation upon involuntary termination without cause.

7. REGULATORY COMPLIANCE AND GOVERNANCE
Employee must comply with all applicable laws including securities regulations.
Insider trading policy compliance mandatory with quarterly certifications.
Code of conduct acknowledgment required annually with ethics training completion.
Whistleblower protections provided for good faith reporting of violations.
""",
            
            "vendor_services_agreement.txt": """
CLOUD SERVICES AND VENDOR AGREEMENT

1. SERVICE DESCRIPTION AND SPECIFICATIONS
Vendor provides cloud hosting, managed services, and technical support.
Service Level Agreement guarantees ninety-nine point nine percent (99.9%) uptime.
Support includes twenty-four by seven (24x7) monitoring and incident response.
Scalable infrastructure with automatic provisioning and load balancing.

2. PRICING AND BILLING ARRANGEMENTS
Monthly base fee of Twenty Thousand Dollars ($20,000) for standard service tier.
Additional storage charged at fifty cents ($0.50) per gigabyte monthly.
Data transfer fees apply at ten cents ($0.10) per gigabyte for bandwidth overages.
Annual payment discount of ten percent (10%) available with advance payment.

3. DATA SECURITY AND PROTECTION MEASURES
All customer data encrypted using Advanced Encryption Standard (AES-256).
Encryption applies to data at rest, in transit, and during processing operations.
Access controls implement role-based permissions and multi-factor authentication.
Security monitoring includes intrusion detection and anomaly analysis systems.

4. COMPLIANCE AND CERTIFICATION REQUIREMENTS
Vendor maintains SOC 2 Type II certification with annual independent audits.
HIPAA Business Associate Agreement executed for protected health information.
PCI DSS Level 1 compliance for payment card data processing and storage.
Regular penetration testing and vulnerability assessments by certified firms.

5. BACKUP, RECOVERY, AND BUSINESS CONTINUITY
Automated daily backups with retention period of ninety (90) days minimum.
Geographically distributed backup storage in multiple availability zones.
Disaster recovery site located minimum five hundred (500) miles from primary.
Recovery Time Objective (RTO) of four (4) hours for critical system restoration.

6. SERVICE LEVEL AGREEMENTS AND REMEDIES
Monthly uptime calculation excludes scheduled maintenance windows.
Service credits of five percent (5%) of monthly fees for each hour below SLA.
Priority support response times: Critical (1 hour), High (4 hours), Normal (24 hours).
Root cause analysis provided for all incidents affecting service availability.

7. DATA OWNERSHIP AND PORTABILITY
Customer retains all rights, title, and interest in Customer Data.
Vendor may access Customer Data solely to provide contracted services.
Data export capabilities provided in standard formats upon termination.
Secure data destruction within thirty (30) days following contract expiration.
""",
            
            "intellectual_property_agreement.txt": """
INTELLECTUAL PROPERTY LICENSING AGREEMENT

1. INTELLECTUAL PROPERTY DEFINITIONS
"Licensed IP" includes patents, trademarks, copyrights, and trade secrets.
"Patent Rights" means all patents and patent applications owned by Licensor.
"Know-How" includes technical information, processes, and proprietary methods.
"Improvements" means enhancements or modifications to Licensed IP.

2. GRANT OF RIGHTS AND RESTRICTIONS
Licensor grants Licensee exclusive license to Licensed IP in designated territory.
License includes right to manufacture, use, sell, and distribute products.
Sublicensing permitted with written consent and revenue sharing requirements.
Field of use restricted to medical device applications and related services.

3. ROYALTY AND PAYMENT OBLIGATIONS
Licensee pays running royalty of eight percent (8%) on Net Sales of Licensed Products.
Minimum annual royalty of Five Hundred Thousand Dollars ($500,000) required.
Royalty payments due quarterly within sixty (60) days of quarter end.
Audit rights reserved with certified public accountant access to relevant records.

4. DEVELOPMENT AND COMMERCIALIZATION
Licensee commits to diligent commercialization efforts using best commercial practices.
Product launch required within thirty-six (36) months of effective date.
Failure to meet commercialization milestones may result in license conversion to non-exclusive.
Regular progress reports required detailing development activities and market penetration.

5. INTELLECTUAL PROPERTY ENFORCEMENT
Licensor retains primary responsibility for patent prosecution and maintenance.
Joint enforcement rights for patent infringement with cost sharing provisions.
Licensee must notify Licensor of potential infringement within thirty (30) days.
Defense cooperation required for validity challenges and patent disputes.

6. CONFIDENTIALITY AND TRADE SECRETS
Trade secret protection maintained through reasonable security measures.
Employee and contractor confidentiality agreements required for access.
Disclosure limited to employees with legitimate business need-to-know.
Trade secret obligations survive termination indefinitely.

7. TERM, TERMINATION, AND SURVIVAL
Initial term of ten (10) years with renewal options subject to renegotiation.
Termination for material breach with sixty (60) day cure period.
Patent license survives termination for products sold during agreement term.
Confidentiality, audit, and indemnification provisions survive termination.
"""
        }
        
        # Save CUAD-style contract documents
        for filename, content in cuad_contracts.items():
            filepath = os.path.join(PDF_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"Created {len(cuad_contracts)} CUAD-style contract documents")
        return list(cuad_contracts.keys())
    
    def chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk = ' '.join(chunk_words)
            if len(chunk.strip()) > 0:
                chunks.append(chunk)
                
        return chunks
    
    def process_documents(self) -> Dict:
        """Process all documents in the PDF directory"""
        documents = []
        metadata = []
        
        # Check if we have documents, if not create samples
        if not os.path.exists(PDF_DIR) or not os.listdir(PDF_DIR):
            print("No documents found, creating CUAD contract documents...")
            self.download_cuad_contracts()
        
        # Process each document
        for filename in os.listdir(PDF_DIR):
            if filename.endswith(('.txt', '.pdf')):
                filepath = os.path.join(PDF_DIR, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Create chunks
                    chunks = self.chunk_text(content)
                    
                    for i, chunk in enumerate(chunks):
                        documents.append(chunk)
                        metadata.append({
                            'filename': filename,
                            'chunk_id': i,
                            'total_chunks': len(chunks),
                            'char_count': len(chunk)
                        })
                    
                    print(f"Processed {filename}: {len(chunks)} chunks")
                    
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        self.document_chunks = documents
        self.chunk_metadata = metadata
        
        return {
            'total_documents': len(set(meta['filename'] for meta in metadata)),
            'total_chunks': len(documents),
            'processed_files': list(set(meta['filename'] for meta in metadata))
        }
    
    def create_vector_store(self):
        """Create TF-IDF vector store from processed documents"""
        if not self.document_chunks:
            self.process_documents()
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        
        # Fit and transform documents
        tfidf_matrix = self.vectorizer.fit_transform(self.document_chunks)
        
        # Save vector store
        os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
        
        # Save vectorizer
        with open(os.path.join(VECTOR_STORE_DIR, 'vectorizer.pkl'), 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        # Save TF-IDF matrix
        with open(os.path.join(VECTOR_STORE_DIR, 'tfidf_matrix.pkl'), 'wb') as f:
            pickle.dump(tfidf_matrix, f)
        
        # Save documents and metadata
        with open(os.path.join(VECTOR_STORE_DIR, 'documents.json'), 'w') as f:
            json.dump({
                'chunks': self.document_chunks,
                'metadata': self.chunk_metadata
            }, f, indent=2)
        
        print(f"Vector store created with {len(self.document_chunks)} chunks")
        return tfidf_matrix
    
    def load_vector_store(self):
        """Load existing vector store"""
        try:
            # Load vectorizer
            with open(os.path.join(VECTOR_STORE_DIR, 'vectorizer.pkl'), 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            # Load TF-IDF matrix
            with open(os.path.join(VECTOR_STORE_DIR, 'tfidf_matrix.pkl'), 'rb') as f:
                tfidf_matrix = pickle.load(f)
            
            # Load documents and metadata
            with open(os.path.join(VECTOR_STORE_DIR, 'documents.json'), 'r') as f:
                data = json.load(f)
                self.document_chunks = data['chunks']
                self.chunk_metadata = data['metadata']
            
            return tfidf_matrix
        
        except FileNotFoundError:
            print("Vector store not found, creating new one...")
            return self.create_vector_store()
    
    def search_documents(self, query: str, k: int = 5):
        """Search for relevant document chunks"""
        if self.vectorizer is None:
            tfidf_matrix = self.load_vector_store()
        else:
            with open(os.path.join(VECTOR_STORE_DIR, 'tfidf_matrix.pkl'), 'rb') as f:
                tfidf_matrix = pickle.load(f)
        
        # Transform query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # Get top k results
        top_indices = np.argsort(similarities)[::-1][:k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only include relevant results
                results.append({
                    'content': self.document_chunks[idx],
                    'metadata': self.chunk_metadata[idx],
                    'similarity': float(similarities[idx])
                })
        
        return results

if __name__ == "__main__":
    processor = PDFProcessor()
    result = processor.process_documents()
    print(f"Processing complete: {result}")
    processor.create_vector_store()
    print("Vector store created successfully!")