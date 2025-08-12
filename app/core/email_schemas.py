"""
Email-related Pydantic schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class SendEmailRequest(BaseModel):
    to_email: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, max_length=200, description="Email subject")
    message: str = Field(..., min_length=1, max_length=5000, description="Email message content")
    html_message: Optional[str] = Field(None, max_length=10000, description="Optional HTML message content")


class ContactFormRequest(BaseModel):
    to_email: EmailStr = Field(..., description="Recipient email address")
    sender_name: str = Field(..., min_length=1, max_length=100, description="Sender's name")
    sender_email: EmailStr = Field(..., description="Sender's email address")
    subject: str = Field(..., min_length=1, max_length=200, description="Message subject")
    message: str = Field(..., min_length=1, max_length=5000, description="Message content")


class WelcomeEmailRequest(BaseModel):
    to_email: EmailStr = Field(..., description="New user's email address")
    name: Optional[str] = Field(None, max_length=100, description="User's name")


class EmailResponse(BaseModel):
    success: bool = True
    message: str
    recipient: str


class EmailErrorResponse(BaseModel):
    success: bool = False
    error: str
    error_code: str