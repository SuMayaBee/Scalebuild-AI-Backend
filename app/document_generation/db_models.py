from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, func
from app.core.database import Base

class BusinessProposal(Base):
    __tablename__ = "business_proposals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String, nullable=False)
    client_name = Column(String, nullable=False)
    project_title = Column(String, nullable=False)
    ai_generated_content = Column(Text, nullable=False)
    input_data = Column(JSON, nullable=False)  # Store original request data
    docs_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class PartnershipAgreement(Base):
    __tablename__ = "partnership_agreements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    party1_name = Column(String, nullable=False)
    party2_name = Column(String, nullable=False)
    partnership_purpose = Column(String, nullable=False)
    ai_generated_content = Column(Text, nullable=False)
    input_data = Column(JSON, nullable=False)
    docs_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class NDA(Base):
    __tablename__ = "ndas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    disclosing_party = Column(String, nullable=False)
    receiving_party = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    ai_generated_content = Column(Text, nullable=False)
    input_data = Column(JSON, nullable=False)
    docs_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contract_type = Column(String, nullable=False)
    party1_name = Column(String, nullable=False)
    party2_name = Column(String, nullable=False)
    service_description = Column(String, nullable=False)
    ai_generated_content = Column(Text, nullable=False)
    input_data = Column(JSON, nullable=False)
    docs_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class TermsOfService(Base):
    __tablename__ = "terms_of_service"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String, nullable=False)
    website_url = Column(String, nullable=False)
    service_description = Column(String, nullable=False)
    ai_generated_content = Column(Text, nullable=False)
    input_data = Column(JSON, nullable=False)
    docs_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class PrivacyPolicy(Base):
    __tablename__ = "privacy_policies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String, nullable=False)
    website_url = Column(String, nullable=False)
    ai_generated_content = Column(Text, nullable=False)
    input_data = Column(JSON, nullable=False)
    docs_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())