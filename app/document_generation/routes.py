from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.storage_service import upload_to_gcs
from app.document_generation.models import (
    BusinessProposalRequest, BusinessProposalResponse,
    PartnershipAgreementRequest, PartnershipAgreementResponse,
    NDARequest, NDAResponse,
    ContractRequest, ContractResponse,
    TermsOfServiceRequest, TermsOfServiceResponse,
    PrivacyPolicyRequest, PrivacyPolicyResponse,
    DocumentUpdateRequest,
    DocumentFileUploadResponse
)
from app.document_generation.services.document_generation_services import (
    generate_business_proposal,
    generate_partnership_agreement,
    generate_nda,
    generate_contract,
    generate_terms_of_service,
    generate_privacy_policy
)
from app.document_generation.crud import (
    create_business_proposal, get_business_proposal, get_user_business_proposals,
    update_business_proposal_content, update_business_proposal_docs_url,
    create_partnership_agreement, get_partnership_agreement, get_user_partnership_agreements,
    update_partnership_agreement_content, update_partnership_agreement_docs_url,
    create_nda, get_nda, get_user_ndas,
    update_nda_content, update_nda_docs_url,
    create_contract, get_contract, get_user_contracts,
    update_contract_content, update_contract_docs_url,
    create_terms_of_service, get_terms_of_service, get_user_terms_of_service,
    update_terms_of_service_content, update_terms_of_service_docs_url,
    create_privacy_policy, get_privacy_policy, get_user_privacy_policies,
    update_privacy_policy_content, update_privacy_policy_docs_url
)
from typing import List
import io
import uuid

router = APIRouter()

# ==================== BUSINESS PROPOSAL ENDPOINTS ====================

@router.post("/documents/business-proposal", response_model=BusinessProposalResponse)
async def create_business_proposal_endpoint(request: BusinessProposalRequest, db: Session = Depends(get_db)):
    """Generate business proposal and save to database"""
    try:
        ai_content = await generate_business_proposal(request.dict())
        
        proposal = create_business_proposal(
            db=db,
            user_id=request.user_id,
            company_name=request.company_name,
            client_name=request.client_name,
            project_title=request.project_title,
            ai_generated_content=ai_content,
            input_data=request.dict()
        )
        
        return BusinessProposalResponse(
            id=proposal.id, user_id=proposal.user_id, company_name=proposal.company_name,
            client_name=proposal.client_name, project_title=proposal.project_title,
            ai_generated_content=proposal.ai_generated_content, input_data=proposal.input_data,
            docs_url=proposal.docs_url, created_at=proposal.created_at, updated_at=proposal.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/business-proposal/{proposal_id}", response_model=BusinessProposalResponse)
async def get_business_proposal_endpoint(proposal_id: int, db: Session = Depends(get_db)):
    """Get business proposal by ID"""
    proposal = get_business_proposal(db, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Business proposal not found")
    
    return BusinessProposalResponse(
        id=proposal.id, user_id=proposal.user_id, company_name=proposal.company_name,
        client_name=proposal.client_name, project_title=proposal.project_title,
        ai_generated_content=proposal.ai_generated_content, input_data=proposal.input_data,
        docs_url=proposal.docs_url, created_at=proposal.created_at, updated_at=proposal.updated_at
    )

@router.get("/documents/business-proposal/user/{user_id}", response_model=List[BusinessProposalResponse])
async def get_user_business_proposals_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Get all business proposals for a user"""
    proposals = get_user_business_proposals(db, user_id)
    return [
        BusinessProposalResponse(
            id=p.id, user_id=p.user_id, company_name=p.company_name,
            client_name=p.client_name, project_title=p.project_title,
            ai_generated_content=p.ai_generated_content, input_data=p.input_data,
            docs_url=p.docs_url, created_at=p.created_at, updated_at=p.updated_at
        ) for p in proposals
    ]

@router.put("/documents/business-proposal/{proposal_id}", response_model=BusinessProposalResponse)
async def update_business_proposal_endpoint(proposal_id: int, request: DocumentUpdateRequest, db: Session = Depends(get_db)):
    """Update business proposal content"""
    proposal = update_business_proposal_content(db, proposal_id, request.ai_generated_content)
    if not proposal:
        raise HTTPException(status_code=404, detail="Business proposal not found")
    
    return BusinessProposalResponse(
        id=proposal.id, user_id=proposal.user_id, company_name=proposal.company_name,
        client_name=proposal.client_name, project_title=proposal.project_title,
        ai_generated_content=proposal.ai_generated_content, input_data=proposal.input_data,
        docs_url=proposal.docs_url, created_at=proposal.created_at, updated_at=proposal.updated_at
    )

@router.post("/documents/upload/business-proposal/{proposal_id}", response_model=DocumentFileUploadResponse)
async def upload_business_proposal_file(proposal_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload business proposal file to GCS and update database"""
    try:
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'docx'
        unique_filename = f"business_proposal_{proposal_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        
        file_content = await file.read()
        file_obj = io.BytesIO(file_content)
        
        docs_url = upload_to_gcs(file_obj, unique_filename, file.content_type or "application/octet-stream")
        
        proposal = update_business_proposal_docs_url(db, proposal_id, docs_url)
        if not proposal:
            raise HTTPException(status_code=404, detail="Business proposal not found")
        
        return DocumentFileUploadResponse(success=True, document_id=proposal_id, docs_url=docs_url)
    except Exception as e:
        return DocumentFileUploadResponse(success=False, document_id=proposal_id, error=str(e))

# ==================== PARTNERSHIP AGREEMENT ENDPOINTS ====================

@router.post("/documents/partnership-agreement", response_model=PartnershipAgreementResponse)
async def create_partnership_agreement_endpoint(request: PartnershipAgreementRequest, db: Session = Depends(get_db)):
    """Generate partnership agreement and save to database"""
    try:
        ai_content = await generate_partnership_agreement(request.dict())
        
        agreement = create_partnership_agreement(
            db=db,
            user_id=request.user_id,
            party1_name=request.party1_name,
            party2_name=request.party2_name,
            partnership_purpose=request.partnership_purpose,
            ai_generated_content=ai_content,
            input_data=request.dict()
        )
        
        return PartnershipAgreementResponse(
            id=agreement.id, user_id=agreement.user_id, party1_name=agreement.party1_name,
            party2_name=agreement.party2_name, partnership_purpose=agreement.partnership_purpose,
            ai_generated_content=agreement.ai_generated_content, input_data=agreement.input_data,
            docs_url=agreement.docs_url, created_at=agreement.created_at, updated_at=agreement.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/partnership-agreement/{agreement_id}", response_model=PartnershipAgreementResponse)
async def get_partnership_agreement_endpoint(agreement_id: int, db: Session = Depends(get_db)):
    """Get partnership agreement by ID"""
    agreement = get_partnership_agreement(db, agreement_id)
    if not agreement:
        raise HTTPException(status_code=404, detail="Partnership agreement not found")
    
    return PartnershipAgreementResponse(
        id=agreement.id, user_id=agreement.user_id, party1_name=agreement.party1_name,
        party2_name=agreement.party2_name, partnership_purpose=agreement.partnership_purpose,
        ai_generated_content=agreement.ai_generated_content, input_data=agreement.input_data,
        docs_url=agreement.docs_url, created_at=agreement.created_at, updated_at=agreement.updated_at
    )

@router.get("/documents/partnership-agreement/user/{user_id}", response_model=List[PartnershipAgreementResponse])
async def get_user_partnership_agreements_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Get all partnership agreements for a user"""
    agreements = get_user_partnership_agreements(db, user_id)
    return [
        PartnershipAgreementResponse(
            id=a.id, user_id=a.user_id, party1_name=a.party1_name,
            party2_name=a.party2_name, partnership_purpose=a.partnership_purpose,
            ai_generated_content=a.ai_generated_content, input_data=a.input_data,
            docs_url=a.docs_url, created_at=a.created_at, updated_at=a.updated_at
        ) for a in agreements
    ]

@router.put("/documents/partnership-agreement/{agreement_id}", response_model=PartnershipAgreementResponse)
async def update_partnership_agreement_endpoint(agreement_id: int, request: DocumentUpdateRequest, db: Session = Depends(get_db)):
    """Update partnership agreement content"""
    agreement = update_partnership_agreement_content(db, agreement_id, request.ai_generated_content)
    if not agreement:
        raise HTTPException(status_code=404, detail="Partnership agreement not found")
    
    return PartnershipAgreementResponse(
        id=agreement.id, user_id=agreement.user_id, party1_name=agreement.party1_name,
        party2_name=agreement.party2_name, partnership_purpose=agreement.partnership_purpose,
        ai_generated_content=agreement.ai_generated_content, input_data=agreement.input_data,
        docs_url=agreement.docs_url, created_at=agreement.created_at, updated_at=agreement.updated_at
    )

@router.post("/documents/upload/partnership-agreement/{agreement_id}", response_model=DocumentFileUploadResponse)
async def upload_partnership_agreement_file(agreement_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload partnership agreement file to GCS and update database"""
    try:
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'docx'
        unique_filename = f"partnership_agreement_{agreement_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        
        file_content = await file.read()
        file_obj = io.BytesIO(file_content)
        
        docs_url = upload_to_gcs(file_obj, unique_filename, file.content_type or "application/octet-stream")
        
        agreement = update_partnership_agreement_docs_url(db, agreement_id, docs_url)
        if not agreement:
            raise HTTPException(status_code=404, detail="Partnership agreement not found")
        
        return DocumentFileUploadResponse(success=True, document_id=agreement_id, docs_url=docs_url)
    except Exception as e:
        return DocumentFileUploadResponse(success=False, document_id=agreement_id, error=str(e))

# ==================== NDA ENDPOINTS ====================

@router.post("/documents/nda", response_model=NDAResponse)
async def create_nda_endpoint(request: NDARequest, db: Session = Depends(get_db)):
    """Generate NDA and save to database"""
    try:
        ai_content = await generate_nda(request.dict())
        
        nda = create_nda(
            db=db,
            user_id=request.user_id,
            disclosing_party=request.disclosing_party,
            receiving_party=request.receiving_party,
            purpose=request.purpose,
            ai_generated_content=ai_content,
            input_data=request.dict()
        )
        
        return NDAResponse(
            id=nda.id, user_id=nda.user_id, disclosing_party=nda.disclosing_party,
            receiving_party=nda.receiving_party, purpose=nda.purpose,
            ai_generated_content=nda.ai_generated_content, input_data=nda.input_data,
            docs_url=nda.docs_url, created_at=nda.created_at, updated_at=nda.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/nda/{nda_id}", response_model=NDAResponse)
async def get_nda_endpoint(nda_id: int, db: Session = Depends(get_db)):
    """Get NDA by ID"""
    nda = get_nda(db, nda_id)
    if not nda:
        raise HTTPException(status_code=404, detail="NDA not found")
    
    return NDAResponse(
        id=nda.id, user_id=nda.user_id, disclosing_party=nda.disclosing_party,
        receiving_party=nda.receiving_party, purpose=nda.purpose,
        ai_generated_content=nda.ai_generated_content, input_data=nda.input_data,
        docs_url=nda.docs_url, created_at=nda.created_at, updated_at=nda.updated_at
    )

@router.get("/documents/nda/user/{user_id}", response_model=List[NDAResponse])
async def get_user_ndas_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Get all NDAs for a user"""
    ndas = get_user_ndas(db, user_id)
    return [
        NDAResponse(
            id=n.id, user_id=n.user_id, disclosing_party=n.disclosing_party,
            receiving_party=n.receiving_party, purpose=n.purpose,
            ai_generated_content=n.ai_generated_content, input_data=n.input_data,
            docs_url=n.docs_url, created_at=n.created_at, updated_at=n.updated_at
        ) for n in ndas
    ]

@router.put("/documents/nda/{nda_id}", response_model=NDAResponse)
async def update_nda_endpoint(nda_id: int, request: DocumentUpdateRequest, db: Session = Depends(get_db)):
    """Update NDA content"""
    nda = update_nda_content(db, nda_id, request.ai_generated_content)
    if not nda:
        raise HTTPException(status_code=404, detail="NDA not found")
    
    return NDAResponse(
        id=nda.id, user_id=nda.user_id, disclosing_party=nda.disclosing_party,
        receiving_party=nda.receiving_party, purpose=nda.purpose,
        ai_generated_content=nda.ai_generated_content, input_data=nda.input_data,
        docs_url=nda.docs_url, created_at=nda.created_at, updated_at=nda.updated_at
    )

@router.post("/documents/upload/nda/{nda_id}", response_model=DocumentFileUploadResponse)
async def upload_nda_file(nda_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload NDA file to GCS and update database"""
    try:
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'docx'
        unique_filename = f"nda_{nda_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        
        file_content = await file.read()
        file_obj = io.BytesIO(file_content)
        
        docs_url = upload_to_gcs(file_obj, unique_filename, file.content_type or "application/octet-stream")
        
        nda = update_nda_docs_url(db, nda_id, docs_url)
        if not nda:
            raise HTTPException(status_code=404, detail="NDA not found")
        
        return DocumentFileUploadResponse(success=True, document_id=nda_id, docs_url=docs_url)
    except Exception as e:
        return DocumentFileUploadResponse(success=False, document_id=nda_id, error=str(e))

# ==================== CONTRACT ENDPOINTS ====================

@router.post("/documents/contract", response_model=ContractResponse)
async def create_contract_endpoint(request: ContractRequest, db: Session = Depends(get_db)):
    """Generate contract and save to database"""
    try:
        ai_content = await generate_contract(request.dict())
        
        contract = create_contract(
            db=db,
            user_id=request.user_id,
            contract_type=request.contract_type,
            party1_name=request.party1_name,
            party2_name=request.party2_name,
            service_description=request.service_description,
            ai_generated_content=ai_content,
            input_data=request.dict()
        )
        
        return ContractResponse(
            id=contract.id, user_id=contract.user_id, contract_type=contract.contract_type,
            party1_name=contract.party1_name, party2_name=contract.party2_name,
            service_description=contract.service_description,
            ai_generated_content=contract.ai_generated_content, input_data=contract.input_data,
            docs_url=contract.docs_url, created_at=contract.created_at, updated_at=contract.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/contract/{contract_id}", response_model=ContractResponse)
async def get_contract_endpoint(contract_id: int, db: Session = Depends(get_db)):
    """Get contract by ID"""
    contract = get_contract(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    return ContractResponse(
        id=contract.id, user_id=contract.user_id, contract_type=contract.contract_type,
        party1_name=contract.party1_name, party2_name=contract.party2_name,
        service_description=contract.service_description,
        ai_generated_content=contract.ai_generated_content, input_data=contract.input_data,
        docs_url=contract.docs_url, created_at=contract.created_at, updated_at=contract.updated_at
    )

@router.get("/documents/contract/user/{user_id}", response_model=List[ContractResponse])
async def get_user_contracts_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Get all contracts for a user"""
    contracts = get_user_contracts(db, user_id)
    return [
        ContractResponse(
            id=c.id, user_id=c.user_id, contract_type=c.contract_type,
            party1_name=c.party1_name, party2_name=c.party2_name,
            service_description=c.service_description,
            ai_generated_content=c.ai_generated_content, input_data=c.input_data,
            docs_url=c.docs_url, created_at=c.created_at, updated_at=c.updated_at
        ) for c in contracts
    ]

@router.put("/documents/contract/{contract_id}", response_model=ContractResponse)
async def update_contract_endpoint(contract_id: int, request: DocumentUpdateRequest, db: Session = Depends(get_db)):
    """Update contract content"""
    contract = update_contract_content(db, contract_id, request.ai_generated_content)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    return ContractResponse(
        id=contract.id, user_id=contract.user_id, contract_type=contract.contract_type,
        party1_name=contract.party1_name, party2_name=contract.party2_name,
        service_description=contract.service_description,
        ai_generated_content=contract.ai_generated_content, input_data=contract.input_data,
        docs_url=contract.docs_url, created_at=contract.created_at, updated_at=contract.updated_at
    )

@router.post("/documents/upload/contract/{contract_id}", response_model=DocumentFileUploadResponse)
async def upload_contract_file(contract_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload contract file to GCS and update database"""
    try:
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'docx'
        unique_filename = f"contract_{contract_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        
        file_content = await file.read()
        file_obj = io.BytesIO(file_content)
        
        docs_url = upload_to_gcs(file_obj, unique_filename, file.content_type or "application/octet-stream")
        
        contract = update_contract_docs_url(db, contract_id, docs_url)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        return DocumentFileUploadResponse(success=True, document_id=contract_id, docs_url=docs_url)
    except Exception as e:
        return DocumentFileUploadResponse(success=False, document_id=contract_id, error=str(e))

# ==================== TERMS OF SERVICE ENDPOINTS ====================

@router.post("/documents/terms-of-service", response_model=TermsOfServiceResponse)
async def create_terms_of_service_endpoint(request: TermsOfServiceRequest, db: Session = Depends(get_db)):
    """Generate terms of service and save to database"""
    try:
        ai_content = await generate_terms_of_service(request.dict())
        
        terms = create_terms_of_service(
            db=db,
            user_id=request.user_id,
            company_name=request.company_name,
            website_url=request.website_url,
            service_description=request.service_description,
            ai_generated_content=ai_content,
            input_data=request.dict()
        )
        
        return TermsOfServiceResponse(
            id=terms.id, user_id=terms.user_id, company_name=terms.company_name,
            website_url=terms.website_url, service_description=terms.service_description,
            ai_generated_content=terms.ai_generated_content, input_data=terms.input_data,
            docs_url=terms.docs_url, created_at=terms.created_at, updated_at=terms.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/terms-of-service/{terms_id}", response_model=TermsOfServiceResponse)
async def get_terms_of_service_endpoint(terms_id: int, db: Session = Depends(get_db)):
    """Get terms of service by ID"""
    terms = get_terms_of_service(db, terms_id)
    if not terms:
        raise HTTPException(status_code=404, detail="Terms of service not found")
    
    return TermsOfServiceResponse(
        id=terms.id, user_id=terms.user_id, company_name=terms.company_name,
        website_url=terms.website_url, service_description=terms.service_description,
        ai_generated_content=terms.ai_generated_content, input_data=terms.input_data,
        docs_url=terms.docs_url, created_at=terms.created_at, updated_at=terms.updated_at
    )

@router.get("/documents/terms-of-service/user/{user_id}", response_model=List[TermsOfServiceResponse])
async def get_user_terms_of_service_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Get all terms of service for a user"""
    terms_list = get_user_terms_of_service(db, user_id)
    return [
        TermsOfServiceResponse(
            id=t.id, user_id=t.user_id, company_name=t.company_name,
            website_url=t.website_url, service_description=t.service_description,
            ai_generated_content=t.ai_generated_content, input_data=t.input_data,
            docs_url=t.docs_url, created_at=t.created_at, updated_at=t.updated_at
        ) for t in terms_list
    ]

@router.put("/documents/terms-of-service/{terms_id}", response_model=TermsOfServiceResponse)
async def update_terms_of_service_endpoint(terms_id: int, request: DocumentUpdateRequest, db: Session = Depends(get_db)):
    """Update terms of service content"""
    terms = update_terms_of_service_content(db, terms_id, request.ai_generated_content)
    if not terms:
        raise HTTPException(status_code=404, detail="Terms of service not found")
    
    return TermsOfServiceResponse(
        id=terms.id, user_id=terms.user_id, company_name=terms.company_name,
        website_url=terms.website_url, service_description=terms.service_description,
        ai_generated_content=terms.ai_generated_content, input_data=terms.input_data,
        docs_url=terms.docs_url, created_at=terms.created_at, updated_at=terms.updated_at
    )

@router.post("/documents/upload/terms-of-service/{terms_id}", response_model=DocumentFileUploadResponse)
async def upload_terms_of_service_file(terms_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload terms of service file to GCS and update database"""
    try:
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'docx'
        unique_filename = f"terms_of_service_{terms_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        
        file_content = await file.read()
        file_obj = io.BytesIO(file_content)
        
        docs_url = upload_to_gcs(file_obj, unique_filename, file.content_type or "application/octet-stream")
        
        terms = update_terms_of_service_docs_url(db, terms_id, docs_url)
        if not terms:
            raise HTTPException(status_code=404, detail="Terms of service not found")
        
        return DocumentFileUploadResponse(success=True, document_id=terms_id, docs_url=docs_url)
    except Exception as e:
        return DocumentFileUploadResponse(success=False, document_id=terms_id, error=str(e))

# ==================== PRIVACY POLICY ENDPOINTS ====================

@router.post("/documents/privacy-policy", response_model=PrivacyPolicyResponse)
async def create_privacy_policy_endpoint(request: PrivacyPolicyRequest, db: Session = Depends(get_db)):
    """Generate privacy policy and save to database"""
    try:
        ai_content = await generate_privacy_policy(request.dict())
        
        policy = create_privacy_policy(
            db=db,
            user_id=request.user_id,
            company_name=request.company_name,
            website_url=request.website_url,
            ai_generated_content=ai_content,
            input_data=request.dict()
        )
        
        return PrivacyPolicyResponse(
            id=policy.id, user_id=policy.user_id, company_name=policy.company_name,
            website_url=policy.website_url, ai_generated_content=policy.ai_generated_content,
            input_data=policy.input_data, docs_url=policy.docs_url,
            created_at=policy.created_at, updated_at=policy.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/privacy-policy/{policy_id}", response_model=PrivacyPolicyResponse)
async def get_privacy_policy_endpoint(policy_id: int, db: Session = Depends(get_db)):
    """Get privacy policy by ID"""
    policy = get_privacy_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Privacy policy not found")
    
    return PrivacyPolicyResponse(
        id=policy.id, user_id=policy.user_id, company_name=policy.company_name,
        website_url=policy.website_url, ai_generated_content=policy.ai_generated_content,
        input_data=policy.input_data, docs_url=policy.docs_url,
        created_at=policy.created_at, updated_at=policy.updated_at
    )

@router.get("/documents/privacy-policy/user/{user_id}", response_model=List[PrivacyPolicyResponse])
async def get_user_privacy_policies_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Get all privacy policies for a user"""
    policies = get_user_privacy_policies(db, user_id)
    return [
        PrivacyPolicyResponse(
            id=p.id, user_id=p.user_id, company_name=p.company_name,
            website_url=p.website_url, ai_generated_content=p.ai_generated_content,
            input_data=p.input_data, docs_url=p.docs_url,
            created_at=p.created_at, updated_at=p.updated_at
        ) for p in policies
    ]

@router.put("/documents/privacy-policy/{policy_id}", response_model=PrivacyPolicyResponse)
async def update_privacy_policy_endpoint(policy_id: int, request: DocumentUpdateRequest, db: Session = Depends(get_db)):
    """Update privacy policy content"""
    policy = update_privacy_policy_content(db, policy_id, request.ai_generated_content)
    if not policy:
        raise HTTPException(status_code=404, detail="Privacy policy not found")
    
    return PrivacyPolicyResponse(
        id=policy.id, user_id=policy.user_id, company_name=policy.company_name,
        website_url=policy.website_url, ai_generated_content=policy.ai_generated_content,
        input_data=policy.input_data, docs_url=policy.docs_url,
        created_at=policy.created_at, updated_at=policy.updated_at
    )

@router.post("/documents/upload/privacy-policy/{policy_id}", response_model=DocumentFileUploadResponse)
async def upload_privacy_policy_file(policy_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload privacy policy file to GCS and update database"""
    try:
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'docx'
        unique_filename = f"privacy_policy_{policy_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        
        file_content = await file.read()
        file_obj = io.BytesIO(file_content)
        
        docs_url = upload_to_gcs(file_obj, unique_filename, file.content_type or "application/octet-stream")
        
        policy = update_privacy_policy_docs_url(db, policy_id, docs_url)
        if not policy:
            raise HTTPException(status_code=404, detail="Privacy policy not found")
        
        return DocumentFileUploadResponse(success=True, document_id=policy_id, docs_url=docs_url)
    except Exception as e:
        return DocumentFileUploadResponse(success=False, document_id=policy_id, error=str(e))

# ==================== UTILITY ENDPOINTS ====================

@router.get("/documents/types")
async def get_document_types():
    """Get all available document types"""
    return {
        "document_types": [
            {
                "type": "business_proposal",
                "name": "Business Proposal",
                "description": "Comprehensive business proposals for client projects"
            },
            {
                "type": "partnership_agreement",
                "name": "Partnership Agreement",
                "description": "Legal partnership agreements between two parties"
            },
            {
                "type": "nda",
                "name": "Non-Disclosure Agreement",
                "description": "Confidentiality agreements to protect sensitive information"
            },
            {
                "type": "contract",
                "name": "Contract",
                "description": "Various types of contracts (service, employment, vendor)"
            },
            {
                "type": "terms_of_service",
                "name": "Terms of Service",
                "description": "Legal terms governing the use of websites and services"
            },
            {
                "type": "privacy_policy",
                "name": "Privacy Policy",
                "description": "Legal documents outlining data collection and privacy practices"
            }
        ]
    }