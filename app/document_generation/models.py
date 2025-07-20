from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

# Request Models
class BusinessProposalRequest(BaseModel):
    user_id: int
    company_name: str
    client_name: str
    project_title: str
    project_description: str
    services_offered: List[str]
    timeline: str
    budget_range: str
    contact_person: str
    contact_email: str
    logo_url: Optional[str] = None

class PartnershipAgreementRequest(BaseModel):
    user_id: int
    party1_name: str
    party1_address: str
    party2_name: str
    party2_address: str
    partnership_purpose: str
    partnership_duration: str
    profit_sharing_ratio: str
    responsibilities_party1: List[str]
    responsibilities_party2: List[str]
    effective_date: str
    logo_url: Optional[str] = None

class NDARequest(BaseModel):
    user_id: int
    disclosing_party: str
    receiving_party: str
    purpose: str
    confidential_info_description: str
    duration: str
    governing_law: str
    effective_date: str
    logo_url: Optional[str] = None

class ContractRequest(BaseModel):
    user_id: int
    contract_type: str  # "service", "employment", "vendor", etc.
    party1_name: str
    party1_address: str
    party2_name: str
    party2_address: str
    service_description: str
    contract_value: str
    payment_terms: str
    duration: str
    deliverables: List[str]
    terms_conditions: List[str]
    effective_date: str
    logo_url: Optional[str] = None

class TermsOfServiceRequest(BaseModel):
    user_id: int
    company_name: str
    website_url: str
    company_address: str
    service_description: str
    user_responsibilities: List[str]
    prohibited_activities: List[str]
    payment_terms: str
    cancellation_policy: str
    limitation_of_liability: str
    governing_law: str
    contact_email: str
    logo_url: Optional[str] = None

class PrivacyPolicyRequest(BaseModel):
    user_id: int
    company_name: str
    website_url: str
    company_address: str
    data_collected: List[str]
    data_usage_purpose: List[str]
    third_party_sharing: str
    data_retention_period: str
    user_rights: List[str]
    cookies_usage: str
    contact_email: str
    governing_law: str
    effective_date: str
    logo_url: Optional[str] = None

# Response Models
class BusinessProposalResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    client_name: str
    project_title: str
    ai_generated_content: str
    input_data: Dict[str, Any]
    docs_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class PartnershipAgreementResponse(BaseModel):
    id: int
    user_id: int
    party1_name: str
    party2_name: str
    partnership_purpose: str
    ai_generated_content: str
    input_data: Dict[str, Any]
    docs_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class NDAResponse(BaseModel):
    id: int
    user_id: int
    disclosing_party: str
    receiving_party: str
    purpose: str
    ai_generated_content: str
    input_data: Dict[str, Any]
    docs_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ContractResponse(BaseModel):
    id: int
    user_id: int
    contract_type: str
    party1_name: str
    party2_name: str
    service_description: str
    ai_generated_content: str
    input_data: Dict[str, Any]
    docs_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class TermsOfServiceResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    website_url: str
    service_description: str
    ai_generated_content: str
    input_data: Dict[str, Any]
    docs_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class PrivacyPolicyResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    website_url: str
    ai_generated_content: str
    input_data: Dict[str, Any]
    docs_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Update Models
class DocumentUpdateRequest(BaseModel):
    ai_generated_content: str

# File Upload Models
class DocumentFileUploadRequest(BaseModel):
    document_id: int
    document_type: str  # "business_proposal", "partnership_agreement", etc.

class DocumentFileUploadResponse(BaseModel):
    success: bool
    document_id: int
    docs_url: Optional[str] = None
    error: Optional[str] = None

# Legacy Response Model (for backward compatibility)
class DocumentResponse(BaseModel):
    document_content: str
    document_type: str
    generated_for: str
    creation_date: str
    word_count: int
    document_url: Optional[str] = None

class DocumentGenerationRequest(BaseModel):
    document_type: str  # "business_proposal", "partnership_agreement", "nda"
    document_data: Dict[str, Any]
