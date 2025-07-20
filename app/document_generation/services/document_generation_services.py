from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import Dict, Any

# OpenAI Model
model = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

# Business Proposal Template
business_proposal_template = """You are a professional business consultant specializing in creating compelling business proposals. Generate a comprehensive business proposal document based on the following information:

Company Name: {company_name}
Client Name: {client_name}
Project Title: {project_title}
Project Description: {project_description}
Services Offered: {services_offered}
Timeline: {timeline}
Budget Range: {budget_range}
Contact Person: {contact_person}
Contact Email: {contact_email}

Create a professional business proposal that includes:

1. Executive Summary
2. Company Overview
3. Project Understanding
4. Proposed Solution
5. Services & Deliverables
6. Timeline & Milestones
7. Investment & Budget
8. Why Choose Us
9. Next Steps
10. Contact Information

The proposal should be persuasive, professional, and tailored to win the client's business. Use formal business language and structure."""

business_proposal_prompt = PromptTemplate.from_template(business_proposal_template)
business_proposal_chain = business_proposal_prompt | model | StrOutputParser()

# Partnership Agreement Template
partnership_agreement_template = """You are a legal document specialist. Generate a comprehensive partnership agreement based on the following information:

Party 1 Name: {party1_name}
Party 1 Address: {party1_address}
Party 2 Name: {party2_name}
Party 2 Address: {party2_address}
Partnership Purpose: {partnership_purpose}
Partnership Duration: {partnership_duration}
Profit Sharing Ratio: {profit_sharing_ratio}
Party 1 Responsibilities: {responsibilities_party1}
Party 2 Responsibilities: {responsibilities_party2}
Effective Date: {effective_date}

Create a professional partnership agreement that includes:

1. Partnership Formation
2. Purpose and Scope
3. Capital Contributions
4. Profit and Loss Distribution
5. Management and Decision Making
6. Responsibilities and Duties
7. Term and Termination
8. Dispute Resolution
9. Miscellaneous Provisions
10. Signatures

Use formal legal language appropriate for a binding partnership agreement."""

partnership_agreement_prompt = PromptTemplate.from_template(partnership_agreement_template)
partnership_agreement_chain = partnership_agreement_prompt | model | StrOutputParser()

# NDA Template
nda_template = """You are a legal document specialist. Generate a comprehensive Non-Disclosure Agreement based on the following information:

Disclosing Party: {disclosing_party}
Receiving Party: {receiving_party}
Purpose: {purpose}
Confidential Information Description: {confidential_info_description}
Duration: {duration}
Governing Law: {governing_law}
Effective Date: {effective_date}

Create a professional NDA that includes:

1. Definition of Confidential Information
2. Obligations of Receiving Party
3. Permitted Uses and Exceptions
4. Term and Termination
5. Return of Materials
6. Remedies and Enforcement
7. General Provisions
8. Signatures

Use formal legal language appropriate for a binding confidentiality agreement."""

nda_prompt = PromptTemplate.from_template(nda_template)
nda_chain = nda_prompt | model | StrOutputParser()

# Contract Template
contract_template = """You are a legal document specialist. Generate a comprehensive {contract_type} contract based on the following information:

Party 1 Name: {party1_name}
Party 1 Address: {party1_address}
Party 2 Name: {party2_name}
Party 2 Address: {party2_address}
Service Description: {service_description}
Contract Value: {contract_value}
Payment Terms: {payment_terms}
Duration: {duration}
Deliverables: {deliverables}
Terms and Conditions: {terms_conditions}
Effective Date: {effective_date}

Create a professional contract that includes:

1. Parties and Recitals
2. Scope of Work/Services
3. Payment Terms and Schedule
4. Performance Standards
5. Term and Termination
6. Intellectual Property Rights
7. Limitation of Liability
8. General Provisions
9. Signatures

Use formal legal language appropriate for a binding contract."""

contract_prompt = PromptTemplate.from_template(contract_template)
contract_chain = contract_prompt | model | StrOutputParser()

# Terms of Service Template
terms_of_service_template = """You are a legal document specialist. Generate comprehensive Terms of Service for a website/service based on the following information:

Company Name: {company_name}
Website URL: {website_url}
Company Address: {company_address}
Service Description: {service_description}
User Responsibilities: {user_responsibilities}
Prohibited Activities: {prohibited_activities}
Payment Terms: {payment_terms}
Cancellation Policy: {cancellation_policy}
Limitation of Liability: {limitation_of_liability}
Governing Law: {governing_law}
Contact Email: {contact_email}

Create professional Terms of Service that include:

1. Acceptance of Terms
2. Description of Service
3. User Accounts and Registration
4. User Conduct and Responsibilities
5. Prohibited Uses
6. Payment and Billing
7. Cancellation and Termination
8. Intellectual Property Rights
9. Disclaimers and Limitation of Liability
10. Governing Law and Dispute Resolution
11. Changes to Terms
12. Contact Information

Use formal legal language appropriate for website terms of service."""

terms_of_service_prompt = PromptTemplate.from_template(terms_of_service_template)
terms_of_service_chain = terms_of_service_prompt | model | StrOutputParser()

# Privacy Policy Template
privacy_policy_template = """You are a legal document specialist. Generate a comprehensive Privacy Policy based on the following information:

Company Name: {company_name}
Website URL: {website_url}
Company Address: {company_address}
Data Collected: {data_collected}
Data Usage Purpose: {data_usage_purpose}
Third Party Sharing: {third_party_sharing}
Data Retention Period: {data_retention_period}
User Rights: {user_rights}
Cookies Usage: {cookies_usage}
Contact Email: {contact_email}
Governing Law: {governing_law}
Effective Date: {effective_date}

Create a professional Privacy Policy that includes:

1. Information We Collect
2. How We Use Your Information
3. Information Sharing and Disclosure
4. Data Security
5. Data Retention
6. Your Rights and Choices
7. Cookies and Tracking Technologies
8. Children's Privacy
9. International Data Transfers
10. Changes to Privacy Policy
11. Contact Information

Use formal legal language appropriate for privacy compliance."""

privacy_policy_prompt = PromptTemplate.from_template(privacy_policy_template)
privacy_policy_chain = privacy_policy_prompt | model | StrOutputParser()

# Generation Functions
async def generate_business_proposal(data: Dict[str, Any]) -> str:
    """Generate business proposal content using AI"""
    services_list = ", ".join(data.get("services_offered", []))
    
    content = ""
    async for chunk in business_proposal_chain.astream({
        "company_name": data.get("company_name"),
        "client_name": data.get("client_name"),
        "project_title": data.get("project_title"),
        "project_description": data.get("project_description"),
        "services_offered": services_list,
        "timeline": data.get("timeline"),
        "budget_range": data.get("budget_range"),
        "contact_person": data.get("contact_person"),
        "contact_email": data.get("contact_email")
    }):
        content += chunk
    
    return content.strip()

async def generate_partnership_agreement(data: Dict[str, Any]) -> str:
    """Generate partnership agreement content using AI"""
    responsibilities_party1 = ", ".join(data.get("responsibilities_party1", []))
    responsibilities_party2 = ", ".join(data.get("responsibilities_party2", []))
    
    content = ""
    async for chunk in partnership_agreement_chain.astream({
        "party1_name": data.get("party1_name"),
        "party1_address": data.get("party1_address"),
        "party2_name": data.get("party2_name"),
        "party2_address": data.get("party2_address"),
        "partnership_purpose": data.get("partnership_purpose"),
        "partnership_duration": data.get("partnership_duration"),
        "profit_sharing_ratio": data.get("profit_sharing_ratio"),
        "responsibilities_party1": responsibilities_party1,
        "responsibilities_party2": responsibilities_party2,
        "effective_date": data.get("effective_date")
    }):
        content += chunk
    
    return content.strip()

async def generate_nda(data: Dict[str, Any]) -> str:
    """Generate NDA content using AI"""
    content = ""
    async for chunk in nda_chain.astream({
        "disclosing_party": data.get("disclosing_party"),
        "receiving_party": data.get("receiving_party"),
        "purpose": data.get("purpose"),
        "confidential_info_description": data.get("confidential_info_description"),
        "duration": data.get("duration"),
        "governing_law": data.get("governing_law"),
        "effective_date": data.get("effective_date")
    }):
        content += chunk
    
    return content.strip()

async def generate_contract(data: Dict[str, Any]) -> str:
    """Generate contract content using AI"""
    deliverables = ", ".join(data.get("deliverables", []))
    terms_conditions = ", ".join(data.get("terms_conditions", []))
    
    content = ""
    async for chunk in contract_chain.astream({
        "contract_type": data.get("contract_type"),
        "party1_name": data.get("party1_name"),
        "party1_address": data.get("party1_address"),
        "party2_name": data.get("party2_name"),
        "party2_address": data.get("party2_address"),
        "service_description": data.get("service_description"),
        "contract_value": data.get("contract_value"),
        "payment_terms": data.get("payment_terms"),
        "duration": data.get("duration"),
        "deliverables": deliverables,
        "terms_conditions": terms_conditions,
        "effective_date": data.get("effective_date")
    }):
        content += chunk
    
    return content.strip()

async def generate_terms_of_service(data: Dict[str, Any]) -> str:
    """Generate terms of service content using AI"""
    user_responsibilities = ", ".join(data.get("user_responsibilities", []))
    prohibited_activities = ", ".join(data.get("prohibited_activities", []))
    
    content = ""
    async for chunk in terms_of_service_chain.astream({
        "company_name": data.get("company_name"),
        "website_url": data.get("website_url"),
        "company_address": data.get("company_address"),
        "service_description": data.get("service_description"),
        "user_responsibilities": user_responsibilities,
        "prohibited_activities": prohibited_activities,
        "payment_terms": data.get("payment_terms"),
        "cancellation_policy": data.get("cancellation_policy"),
        "limitation_of_liability": data.get("limitation_of_liability"),
        "governing_law": data.get("governing_law"),
        "contact_email": data.get("contact_email")
    }):
        content += chunk
    
    return content.strip()

async def generate_privacy_policy(data: Dict[str, Any]) -> str:
    """Generate privacy policy content using AI"""
    data_collected = ", ".join(data.get("data_collected", []))
    data_usage_purpose = ", ".join(data.get("data_usage_purpose", []))
    user_rights = ", ".join(data.get("user_rights", []))
    
    content = ""
    async for chunk in privacy_policy_chain.astream({
        "company_name": data.get("company_name"),
        "website_url": data.get("website_url"),
        "company_address": data.get("company_address"),
        "data_collected": data_collected,
        "data_usage_purpose": data_usage_purpose,
        "third_party_sharing": data.get("third_party_sharing"),
        "data_retention_period": data.get("data_retention_period"),
        "user_rights": user_rights,
        "cookies_usage": data.get("cookies_usage"),
        "contact_email": data.get("contact_email"),
        "governing_law": data.get("governing_law"),
        "effective_date": data.get("effective_date")
    }):
        content += chunk
    
    return content.strip()
