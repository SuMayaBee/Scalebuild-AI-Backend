"""
Resend Email Routes - Simple Email Sending
"""
from fastapi import APIRouter, HTTPException
from app.core.resend_service import resend_email_service
from app.core.resend_schemas import ResendEmailRequest, ResendEmailResponse

router = APIRouter()


@router.post("/send", response_model=ResendEmailResponse)
async def send_resend_email(request: ResendEmailRequest):
    """
    Send an email using Resend API.
    No authentication required.
    
    Required fields:
    - to_email: Recipient email address
    - subject: Email subject
    - html_content: Email body in HTML format
    
    Optional fields:
    - text_content: Plain text version
    - from_email: Custom sender email (uses default if not provided)
    - reply_to: Reply-to email address
    - tags: List of tags for tracking
    """
    try:
        response = resend_email_service.send_email(
            to_email=request.to_email,
            subject=request.subject,
            html_content=request.html_content,
            text_content=request.text_content,
            from_email=request.from_email,
            reply_to=request.reply_to,
            tags=request.tags
        )
        
        return ResendEmailResponse(
            success=True,
            message="Email sent successfully via Resend",
            recipient=request.to_email,
            email_id=response.get('id'),
            data=response
        )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resend email service error: {str(e)}")