from sqlalchemy.orm import Session
from app.document_generation.db_models import (
    BusinessProposal, PartnershipAgreement, NDA, Contract, 
    TermsOfService, PrivacyPolicy
)
from typing import Optional, Dict, Any

# Business Proposal CRUD
def create_business_proposal(
    db: Session,
    user_id: int,
    company_name: str,
    client_name: str,
    project_title: str,
    ai_generated_content: str,
    input_data: Dict[str, Any]
):
    proposal = BusinessProposal(
        user_id=user_id,
        company_name=company_name,
        client_name=client_name,
        project_title=project_title,
        ai_generated_content=ai_generated_content,
        input_data=input_data
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal

def get_business_proposal(db: Session, proposal_id: int):
    return db.query(BusinessProposal).filter(BusinessProposal.id == proposal_id).first()

def get_user_business_proposals(db: Session, user_id: int):
    return db.query(BusinessProposal).filter(BusinessProposal.user_id == user_id).all()

def update_business_proposal_content(db: Session, proposal_id: int, content: str):
    proposal = db.query(BusinessProposal).filter(BusinessProposal.id == proposal_id).first()
    if proposal:
        proposal.ai_generated_content = content
        db.commit()
        db.refresh(proposal)
    return proposal

def update_business_proposal_docs_url(db: Session, proposal_id: int, docs_url: str):
    proposal = db.query(BusinessProposal).filter(BusinessProposal.id == proposal_id).first()
    if proposal:
        proposal.docs_url = docs_url
        db.commit()
        db.refresh(proposal)
    return proposal

# Partnership Agreement CRUD
def create_partnership_agreement(
    db: Session,
    user_id: int,
    party1_name: str,
    party2_name: str,
    partnership_purpose: str,
    ai_generated_content: str,
    input_data: Dict[str, Any]
):
    agreement = PartnershipAgreement(
        user_id=user_id,
        party1_name=party1_name,
        party2_name=party2_name,
        partnership_purpose=partnership_purpose,
        ai_generated_content=ai_generated_content,
        input_data=input_data
    )
    db.add(agreement)
    db.commit()
    db.refresh(agreement)
    return agreement

def get_partnership_agreement(db: Session, agreement_id: int):
    return db.query(PartnershipAgreement).filter(PartnershipAgreement.id == agreement_id).first()

def get_user_partnership_agreements(db: Session, user_id: int):
    return db.query(PartnershipAgreement).filter(PartnershipAgreement.user_id == user_id).all()

def update_partnership_agreement_content(db: Session, agreement_id: int, content: str):
    agreement = db.query(PartnershipAgreement).filter(PartnershipAgreement.id == agreement_id).first()
    if agreement:
        agreement.ai_generated_content = content
        db.commit()
        db.refresh(agreement)
    return agreement

def update_partnership_agreement_docs_url(db: Session, agreement_id: int, docs_url: str):
    agreement = db.query(PartnershipAgreement).filter(PartnershipAgreement.id == agreement_id).first()
    if agreement:
        agreement.docs_url = docs_url
        db.commit()
        db.refresh(agreement)
    return agreement

# NDA CRUD
def create_nda(
    db: Session,
    user_id: int,
    disclosing_party: str,
    receiving_party: str,
    purpose: str,
    ai_generated_content: str,
    input_data: Dict[str, Any]
):
    nda = NDA(
        user_id=user_id,
        disclosing_party=disclosing_party,
        receiving_party=receiving_party,
        purpose=purpose,
        ai_generated_content=ai_generated_content,
        input_data=input_data
    )
    db.add(nda)
    db.commit()
    db.refresh(nda)
    return nda

def get_nda(db: Session, nda_id: int):
    return db.query(NDA).filter(NDA.id == nda_id).first()

def get_user_ndas(db: Session, user_id: int):
    return db.query(NDA).filter(NDA.user_id == user_id).all()

def update_nda_content(db: Session, nda_id: int, content: str):
    nda = db.query(NDA).filter(NDA.id == nda_id).first()
    if nda:
        nda.ai_generated_content = content
        db.commit()
        db.refresh(nda)
    return nda

def update_nda_docs_url(db: Session, nda_id: int, docs_url: str):
    nda = db.query(NDA).filter(NDA.id == nda_id).first()
    if nda:
        nda.docs_url = docs_url
        db.commit()
        db.refresh(nda)
    return nda

# Contract CRUD
def create_contract(
    db: Session,
    user_id: int,
    contract_type: str,
    party1_name: str,
    party2_name: str,
    service_description: str,
    ai_generated_content: str,
    input_data: Dict[str, Any]
):
    contract = Contract(
        user_id=user_id,
        contract_type=contract_type,
        party1_name=party1_name,
        party2_name=party2_name,
        service_description=service_description,
        ai_generated_content=ai_generated_content,
        input_data=input_data
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract

def get_contract(db: Session, contract_id: int):
    return db.query(Contract).filter(Contract.id == contract_id).first()

def get_user_contracts(db: Session, user_id: int):
    return db.query(Contract).filter(Contract.user_id == user_id).all()

def update_contract_content(db: Session, contract_id: int, content: str):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if contract:
        contract.ai_generated_content = content
        db.commit()
        db.refresh(contract)
    return contract

def update_contract_docs_url(db: Session, contract_id: int, docs_url: str):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if contract:
        contract.docs_url = docs_url
        db.commit()
        db.refresh(contract)
    return contract

# Terms of Service CRUD
def create_terms_of_service(
    db: Session,
    user_id: int,
    company_name: str,
    website_url: str,
    service_description: str,
    ai_generated_content: str,
    input_data: Dict[str, Any]
):
    terms = TermsOfService(
        user_id=user_id,
        company_name=company_name,
        website_url=website_url,
        service_description=service_description,
        ai_generated_content=ai_generated_content,
        input_data=input_data
    )
    db.add(terms)
    db.commit()
    db.refresh(terms)
    return terms

def get_terms_of_service(db: Session, terms_id: int):
    return db.query(TermsOfService).filter(TermsOfService.id == terms_id).first()

def get_user_terms_of_service(db: Session, user_id: int):
    return db.query(TermsOfService).filter(TermsOfService.user_id == user_id).all()

def update_terms_of_service_content(db: Session, terms_id: int, content: str):
    terms = db.query(TermsOfService).filter(TermsOfService.id == terms_id).first()
    if terms:
        terms.ai_generated_content = content
        db.commit()
        db.refresh(terms)
    return terms

def update_terms_of_service_docs_url(db: Session, terms_id: int, docs_url: str):
    terms = db.query(TermsOfService).filter(TermsOfService.id == terms_id).first()
    if terms:
        terms.docs_url = docs_url
        db.commit()
        db.refresh(terms)
    return terms

# Privacy Policy CRUD
def create_privacy_policy(
    db: Session,
    user_id: int,
    company_name: str,
    website_url: str,
    ai_generated_content: str,
    input_data: Dict[str, Any]
):
    policy = PrivacyPolicy(
        user_id=user_id,
        company_name=company_name,
        website_url=website_url,
        ai_generated_content=ai_generated_content,
        input_data=input_data
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy

def get_privacy_policy(db: Session, policy_id: int):
    return db.query(PrivacyPolicy).filter(PrivacyPolicy.id == policy_id).first()

def get_user_privacy_policies(db: Session, user_id: int):
    return db.query(PrivacyPolicy).filter(PrivacyPolicy.user_id == user_id).all()

def update_privacy_policy_content(db: Session, policy_id: int, content: str):
    policy = db.query(PrivacyPolicy).filter(PrivacyPolicy.id == policy_id).first()
    if policy:
        policy.ai_generated_content = content
        db.commit()
        db.refresh(policy)
    return policy

def update_privacy_policy_docs_url(db: Session, policy_id: int, docs_url: str):
    policy = db.query(PrivacyPolicy).filter(PrivacyPolicy.id == policy_id).first()
    if policy:
        policy.docs_url = docs_url
        db.commit()
        db.refresh(policy)
    return policy