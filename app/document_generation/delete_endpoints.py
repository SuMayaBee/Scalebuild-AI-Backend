# ==================== DELETE ENDPOINTS ====================

@router.delete("/documents/business-proposal/{proposal_id}")
async def delete_business_proposal_endpoint(proposal_id: int, db: Session = Depends(get_db)):
    """Delete a business proposal by ID"""
    success = delete_business_proposal(db, proposal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Business proposal not found")
    return {"message": "Business proposal deleted successfully", "deleted_id": proposal_id}

@router.delete("/documents/partnership-agreement/{agreement_id}")
async def delete_partnership_agreement_endpoint(agreement_id: int, db: Session = Depends(get_db)):
    """Delete a partnership agreement by ID"""
    success = delete_partnership_agreement(db, agreement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Partnership agreement not found")
    return {"message": "Partnership agreement deleted successfully", "deleted_id": agreement_id}

@router.delete("/documents/nda/{nda_id}")
async def delete_nda_endpoint(nda_id: int, db: Session = Depends(get_db)):
    """Delete an NDA by ID"""
    success = delete_nda(db, nda_id)
    if not success:
        raise HTTPException(status_code=404, detail="NDA not found")
    return {"message": "NDA deleted successfully", "deleted_id": nda_id}

@router.delete("/documents/contract/{contract_id}")
async def delete_contract_endpoint(contract_id: int, db: Session = Depends(get_db)):
    """Delete a contract by ID"""
    success = delete_contract(db, contract_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"message": "Contract deleted successfully", "deleted_id": contract_id}

@router.delete("/documents/terms-of-service/{terms_id}")
async def delete_terms_of_service_endpoint(terms_id: int, db: Session = Depends(get_db)):
    """Delete terms of service by ID"""
    success = delete_terms_of_service(db, terms_id)
    if not success:
        raise HTTPException(status_code=404, detail="Terms of service not found")
    return {"message": "Terms of service deleted successfully", "deleted_id": terms_id}

@router.delete("/documents/privacy-policy/{policy_id}")
async def delete_privacy_policy_endpoint(policy_id: int, db: Session = Depends(get_db)):
    """Delete a privacy policy by ID"""
    success = delete_privacy_policy(db, policy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Privacy policy not found")
    return {"message": "Privacy policy deleted successfully", "deleted_id": policy_id}

@router.delete("/documents/user/{user_id}/all")
async def delete_all_user_documents_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Delete ALL documents for a specific user"""
    try:
        deleted_counts = delete_all_user_documents(db, user_id)
        
        total_deleted = sum(deleted_counts.values())
        
        if total_deleted == 0:
            return {
                "message": "No documents found for this user",
                "user_id": user_id,
                "deleted_counts": deleted_counts,
                "total_deleted": total_deleted
            }
        
        return {
            "message": f"Successfully deleted {total_deleted} documents for user {user_id}",
            "user_id": user_id,
            "deleted_counts": deleted_counts,
            "total_deleted": total_deleted
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user documents: {str(e)}")

# ==================== BULK DELETE ENDPOINTS ====================

@router.delete("/documents/business-proposal/user/{user_id}/all")
async def delete_all_user_business_proposals(user_id: int, db: Session = Depends(get_db)):
    """Delete all business proposals for a specific user"""
    try:
        proposals = get_user_business_proposals(db, user_id)
        deleted_count = 0
        
        for proposal in proposals:
            if delete_business_proposal(db, proposal.id):
                deleted_count += 1
        
        return {
            "message": f"Deleted {deleted_count} business proposals for user {user_id}",
            "user_id": user_id,
            "deleted_count": deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete business proposals: {str(e)}")

@router.delete("/documents/partnership-agreement/user/{user_id}/all")
async def delete_all_user_partnership_agreements(user_id: int, db: Session = Depends(get_db)):
    """Delete all partnership agreements for a specific user"""
    try:
        agreements = get_user_partnership_agreements(db, user_id)
        deleted_count = 0
        
        for agreement in agreements:
            if delete_partnership_agreement(db, agreement.id):
                deleted_count += 1
        
        return {
            "message": f"Deleted {deleted_count} partnership agreements for user {user_id}",
            "user_id": user_id,
            "deleted_count": deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete partnership agreements: {str(e)}")

@router.delete("/documents/nda/user/{user_id}/all")
async def delete_all_user_ndas(user_id: int, db: Session = Depends(get_db)):
    """Delete all NDAs for a specific user"""
    try:
        ndas = get_user_ndas(db, user_id)
        deleted_count = 0
        
        for nda in ndas:
            if delete_nda(db, nda.id):
                deleted_count += 1
        
        return {
            "message": f"Deleted {deleted_count} NDAs for user {user_id}",
            "user_id": user_id,
            "deleted_count": deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete NDAs: {str(e)}")

@router.delete("/documents/contract/user/{user_id}/all")
async def delete_all_user_contracts(user_id: int, db: Session = Depends(get_db)):
    """Delete all contracts for a specific user"""
    try:
        contracts = get_user_contracts(db, user_id)
        deleted_count = 0
        
        for contract in contracts:
            if delete_contract(db, contract.id):
                deleted_count += 1
        
        return {
            "message": f"Deleted {deleted_count} contracts for user {user_id}",
            "user_id": user_id,
            "deleted_count": deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete contracts: {str(e)}")

@router.delete("/documents/terms-of-service/user/{user_id}/all")
async def delete_all_user_terms_of_service(user_id: int, db: Session = Depends(get_db)):
    """Delete all terms of service for a specific user"""
    try:
        terms_list = get_user_terms_of_service(db, user_id)
        deleted_count = 0
        
        for terms in terms_list:
            if delete_terms_of_service(db, terms.id):
                deleted_count += 1
        
        return {
            "message": f"Deleted {deleted_count} terms of service for user {user_id}",
            "user_id": user_id,
            "deleted_count": deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete terms of service: {str(e)}")

@router.delete("/documents/privacy-policy/user/{user_id}/all")
async def delete_all_user_privacy_policies(user_id: int, db: Session = Depends(get_db)):
    """Delete all privacy policies for a specific user"""
    try:
        policies = get_user_privacy_policies(db, user_id)
        deleted_count = 0
        
        for policy in policies:
            if delete_privacy_policy(db, policy.id):
                deleted_count += 1
        
        return {
            "message": f"Deleted {deleted_count} privacy policies for user {user_id}",
            "user_id": user_id,
            "deleted_count": deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete privacy policies: {str(e)}")