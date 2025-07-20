from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from services.document_utils import save_docx_to_gcs
from datetime import datetime

# --- OpenAI Model ---
model = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

# --- Partnership Agreement Template ---
partnership_agreement_template = """You are a legal document specialist. Create a comprehensive Partnership Agreement based on the following details:

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

Generate a formal Partnership Agreement that includes:

1. Partnership Formation
2. Purpose and Scope
3. Duration of Partnership
4. Capital Contributions
5. Profit and Loss Distribution
6. Management and Decision Making
7. Duties and Responsibilities
8. Dissolution Terms
9. Dispute Resolution
10. Governing Law
11. Signatures

Use proper legal language and structure. Include standard clauses for business partnerships."""

partnership_agreement_prompt = PromptTemplate.from_template(partnership_agreement_template)
partnership_agreement_chain = partnership_agreement_prompt | model | StrOutputParser()

async def generate_partnership_agreement(data: dict):
    """Generate a partnership agreement document using GPT-4o and save as .docx with logo"""
    try:
        responsibilities1 = ", ".join(data.get("responsibilities_party1", []))
        responsibilities2 = ", ".join(data.get("responsibilities_party2", []))
        
        document_content = ""
        async for chunk in partnership_agreement_chain.astream({
            "party1_name": data.get("party1_name"),
            "party1_address": data.get("party1_address"),
            "party2_name": data.get("party2_name"),
            "party2_address": data.get("party2_address"),
            "partnership_purpose": data.get("partnership_purpose"),
            "partnership_duration": data.get("partnership_duration"),
            "profit_sharing_ratio": data.get("profit_sharing_ratio"),
            "responsibilities_party1": responsibilities1,
            "responsibilities_party2": responsibilities2,
            "effective_date": data.get("effective_date")
        }):
            document_content += chunk
        
        # Save the document as .docx to GCS with logo
        logo_url = data.get("logo_url")
        document_url = await save_docx_to_gcs(
            document_content, 
            "Partnership Agreement", 
            f"{data.get('party1_name')} & {data.get('party2_name')}",
            logo_url
        )
        
        return {
            "document_content": document_content.strip(),
            "document_url": document_url,
            "document_type": "Partnership Agreement",
            "generated_for": f"{data.get('party1_name')} & {data.get('party2_name')}",
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word_count": len(document_content.split()),
            "format": "DOCX with logo"
        }
    except Exception as e:
        print(f"Error in partnership agreement generation: {e}")
        raise e
