"""
Resend Email Service Pydantic schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any


class ResendEmailRequest(BaseModel):
    to_email: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, max_length=200, description="Email subject")
    html_content: str = Field(..., min_length=1, description="HTML content of the email")
    text_content: Optional[str] = Field(None, description="Optional plain text content")
    from_email: Optional[EmailStr] = Field(None, description="Optional sender email (uses default if not provided)")
    reply_to: Optional[EmailStr] = Field(None, description="Optional reply-to email address")
    tags: Optional[List[Dict[str, str]]] = Field(None, description="Optional tags for email tracking")


class ResendTemplateEmailRequest(BaseModel):
    to_email: EmailStr = Field(..., description="Recipient email address")
    template_type: str = Field(..., description="Template type (welcome, contact, password_reset)")
    from_email: Optional[EmailStr] = Field(None, description="Optional sender email")
    template_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Template variables")


class ResendContactFormRequest(BaseModel):
    to_email: EmailStr = Field(..., description="Recipient email address (where to send the contact form)")
    sender_name: str = Field(..., min_length=1, max_length=100, description="Name of the person sending the message")
    sender_email: EmailStr = Field(..., description="Email of the person sending the message")
    subject: str = Field(..., min_length=1, max_length=200, description="Subject of the message")
    message: str = Field(..., min_length=1, max_length=5000, description="Message content")


class ResendWelcomeEmailRequest(BaseModel):
    to_email: EmailStr = Field(..., description="New user's email address")
    name: Optional[str] = Field(None, max_length=100, description="User's name")


class ResendPasswordResetRequest(BaseModel):
    to_email: EmailStr = Field(..., description="User's email address")
    name: Optional[str] = Field(None, max_length=100, description="User's name")
    reset_token: str = Field(..., description="Password reset token")
    reset_url: str = Field(..., description="Password reset URL")


class ResendEmailResponse(BaseModel):
    success: bool = True
    message: str
    recipient: str
    email_id: Optional[str] = Field(None, description="Resend email ID for tracking")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data from Resend")


class ResendEmailErrorResponse(BaseModel):
    success: bool = False
    error: str
    error_code: Optional[str] = None
    recipient: Optional[str] = None


class ResendHealthResponse(BaseModel):
    status: str
    service: str = "resend"
    configured: bool
    api_key_present: bool