# Compliance rules for policy checking

COMPLIANCE_RULES = {
    "liability_limitation": {
        "title": "Liability Limitation Clauses",
        "description": "Contracts must include appropriate liability limitations and caps",
        "keywords": ["liability", "limitation", "damages", "indemnification", "cap"]
    },
    "termination_rights": {
        "title": "Termination and Cure Period",
        "description": "Clear termination rights with reasonable cure periods",
        "keywords": ["termination", "cure period", "breach", "notice", "immediate termination"]
    },
    "confidentiality_obligations": {
        "title": "Confidentiality and Non-Disclosure",
        "description": "Proper confidentiality protections for proprietary information",
        "keywords": ["confidential", "non-disclosure", "proprietary", "trade secret", "confidentiality"]
    },
    "intellectual_property_rights": {
        "title": "Intellectual Property Ownership",
        "description": "Clear IP ownership and licensing provisions",
        "keywords": ["intellectual property", "patent", "copyright", "trademark", "license", "ownership"]
    },
    "payment_terms": {
        "title": "Payment Terms and Conditions",
        "description": "Defined payment schedules and late payment penalties",
        "keywords": ["payment", "fees", "invoice", "late payment", "interest", "billing"]
    },
    "data_protection_compliance": {
        "title": "Data Protection and Privacy Laws",
        "description": "Compliance with GDPR, CCPA, and other privacy regulations",
        "keywords": ["GDPR", "CCPA", "privacy", "personal data", "data protection", "encryption"]
    },
    "service_level_agreements": {
        "title": "Service Level Commitments",
        "description": "Defined service levels with remedies for non-performance",
        "keywords": ["service level", "SLA", "uptime", "availability", "performance", "remedies"]
    },
    "governing_law_jurisdiction": {
        "title": "Governing Law and Jurisdiction",
        "description": "Clear governing law and dispute resolution mechanisms",
        "keywords": ["governing law", "jurisdiction", "arbitration", "dispute resolution", "court"]
    },
    "insurance_requirements": {
        "title": "Insurance and Coverage Requirements",
        "description": "Adequate insurance coverage with appropriate limits",
        "keywords": ["insurance", "liability coverage", "professional liability", "cyber liability", "coverage"]
    },
    "regulatory_compliance": {
        "title": "Regulatory and Standards Compliance",
        "description": "Compliance with industry regulations and standards",
        "keywords": ["compliance", "regulation", "SOC 2", "HIPAA", "SOX", "PCI DSS", "ISO 27001"]
    },
    "force_majeure": {
        "title": "Force Majeure Provisions",
        "description": "Protection against unforeseeable circumstances",
        "keywords": ["force majeure", "unforeseeable", "act of god", "pandemic", "natural disaster"]
    },
    "assignment_restrictions": {
        "title": "Assignment and Transfer Rights",
        "description": "Restrictions on assignment without consent",
        "keywords": ["assignment", "transfer", "consent", "successor", "change of control"]
    },
    "audit_compliance_reporting": {
        "title": "Audit Rights and Reporting",
        "description": "Audit rights and compliance reporting requirements",
        "keywords": ["audit", "inspection", "records", "compliance report", "certification"]
    },
    "security_incident_response": {
        "title": "Security Incident Notification",
        "description": "Timely notification of security incidents and breaches",
        "keywords": ["security incident", "breach notification", "24 hours", "incident response"]
    },
    "survival_provisions": {
        "title": "Survival of Contract Terms",
        "description": "Terms that survive contract termination",
        "keywords": ["survival", "survive termination", "post-termination", "indefinitely"]
    }
}

def get_all_rules():
    """Return all compliance rules"""
    return COMPLIANCE_RULES

def get_rule(rule_id):
    """Get a specific rule by ID"""
    return COMPLIANCE_RULES.get(rule_id)

def get_rule_keywords():
    """Get all keywords from all rules"""
    keywords = []
    for rule in COMPLIANCE_RULES.values():
        keywords.extend(rule["keywords"])
    return list(set(keywords))