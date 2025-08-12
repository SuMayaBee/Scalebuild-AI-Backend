"""
Email Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from app.core.email_service import email_service
from app.core.email_schemas import (
    SendEmailRequest, 
    ContactFormRequest, 
    WelcomeEmailRequest,
    EmailResponse
)
from app.core.security import get_current_user
from app.auth.db_models import User

router = APIRouter()


@router.post("/send", response_model=EmailResponse)
async def send_email(
    request: SendEmailRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Send a custom email to any recipient.
    Requires authentication.
    """
    try:
        success = email_service.send_email(
            to_email=request.to_email,
            subject=request.subject,
            message=request.message,
            html_message=request.html_message
        )
        
        if success:
            return EmailResponse(
                success=True,
                message="Email sent successfully",
                recipient=request.to_email
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email service error: {str(e)}")


@router.post("/contact", response_model=EmailResponse)
async def send_contact_email(request: ContactFormRequest):
    """
    Send a contact form email.
    Public endpoint - no authentication required.
    """
    try:
        success = email_service.send_template_email(
            to_email=request.to_email,
            template_type="contact",
            sender_name=request.sender_name,
            sender_email=request.sender_email,
            subject=request.subject,
            message=request.message
        )
        
        if success:
            return EmailResponse(
                success=True,
                message="Contact email sent successfully",
                recipient=request.to_email
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to send contact email")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Contact email service error: {str(e)}")


@router.post("/welcome", response_model=EmailResponse)
async def send_welcome_email(
    request: WelcomeEmailRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Send a welcome email to a new user.
    Requires authentication.
    """
    try:
        success = email_service.send_template_email(
            to_email=request.to_email,
            template_type="welcome",
            name=request.name
        )
        
        if success:
            return EmailResponse(
                success=True,
                message="Welcome email sent successfully",
                recipient=request.to_email
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to send welcome email")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Welcome email service error: {str(e)}")


@router.get("/health")
async def email_health_check():
    """Health check for email service."""
    return {
        "status": "healthy", 
        "service": "email",
        "configured": bool(email_service.sender_email and email_service.sender_password)
    }