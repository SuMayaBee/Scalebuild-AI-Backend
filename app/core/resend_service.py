"""
Resend Email Service for sending emails using Resend API
"""
import os
import resend
from typing import Optional, List, Dict, Any
from fastapi import HTTPException


class ResendEmailService:
    def __init__(self):
        # Resend configuration from environment variables
        self.api_key = os.getenv("RESEND_API_KEY")
        self.sender_name = os.getenv("SENDER_NAME", "ScalebuildAI")
        self.sender_email = os.getenv("SENDER_EMAIL", "noreply@yourdomain.com")
        
        if not self.api_key:
            print("⚠️ Warning: Resend API key not configured. Set RESEND_API_KEY in .env")
        else:
            resend.api_key = self.api_key
    
    def send_email(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str,
        text_content: Optional[str] = None,
        from_email: Optional[str] = None,
        reply_to: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Send an email using Resend API.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            text_content: Optional plain text content
            from_email: Optional sender email (defaults to configured sender)
            reply_to: Optional reply-to email address
            tags: Optional list of tags for email tracking
            
        Returns:
            Dict: Response from Resend API containing email ID
            
        Raises:
            HTTPException: If API key is missing or sending fails
        """
        if not self.api_key:
            raise HTTPException(
                status_code=500, 
                detail="Resend API key not configured. Please contact administrator."
            )
        
        try:
            # Prepare email parameters
            email_params = {
                "from": from_email or f"{self.sender_name} <{self.sender_email}>",
                "to": [to_email],
                "subject": subject,
                "html": html_content
            }
            
            # Add optional parameters
            if text_content:
                email_params["text"] = text_content
            
            if reply_to:
                email_params["reply_to"] = [reply_to]
            
            if tags:
                email_params["tags"] = tags
            
            print(f"🔍 Sending email with params: {email_params}")
            print(f"🔑 Using API key: {self.api_key[:10]}..." if self.api_key else "❌ No API key")
            
            # Send email using Resend
            response = resend.Emails.send(email_params)
            
            print(f"📧 Resend API response: {response}")
            
            if response and response.get('id'):
                print(f"✅ Email sent successfully to {to_email} with ID: {response.get('id')}")
                return response
            else:
                print(f"❌ Invalid response from Resend API: {response}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Invalid response from Resend API: {response}"
                )
            
        except Exception as e:
            print(f"❌ Failed to send email via Resend: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to send email: {str(e)}"
            )
    
    def send_template_email(
        self, 
        to_email: str, 
        template_type: str, 
        from_email: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a templated email using predefined templates.
        
        Args:
            to_email: Recipient email address
            template_type: Type of template (welcome, contact, reset_password, etc.)
            from_email: Optional sender email
            **kwargs: Template variables
            
        Returns:
            Dict: Response from Resend API
        """
        templates = {
            "welcome": {
                "subject": "Welcome to ScalebuildAI! 🚀",
                "html_content": f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to ScalebuildAI</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; padding: 20px 0; border-bottom: 2px solid #007bff; }}
        .header h1 {{ color: #007bff; margin: 0; }}
        .content {{ padding: 30px 0; }}
        .features {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .feature-item {{ margin: 10px 0; padding: 10px; background-color: #ffffff; border-left: 4px solid #007bff; }}
        .footer {{ text-align: center; padding: 20px 0; border-top: 1px solid #eee; color: #666; }}
        .btn {{ display: inline-block; padding: 12px 24px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to ScalebuildAI!</h1>
        </div>
        
        <div class="content">
            <h2>Hello {kwargs.get('name', 'there')}! 👋</h2>
            
            <p>We're thrilled to have you join the ScalebuildAI community! Your account has been successfully created with the email address: <strong>{to_email}</strong></p>
            
            <div class="features">
                <h3>🚀 Get started with our powerful AI features:</h3>
                <div class="feature-item">🎨 <strong>AI-Powered Presentations</strong> - Create stunning presentations in minutes</div>
                <div class="feature-item">🎯 <strong>Logo Generation</strong> - Design professional logos with AI</div>
                <div class="feature-item">📄 <strong>Document Creation</strong> - Generate comprehensive business documents</div>
                <div class="feature-item">🎬 <strong>Short Video Generation</strong> - Create engaging video content</div>
            </div>
            
            <p>Ready to transform your business with AI? Start exploring our features today!</p>
            
            <a href="https://scalebuild-new.vercel.app/dashboard" class="btn">Get Started Now</a>
        </div>
        
        <div class="footer">
            <p>If you have any questions, our support team is here to help!</p>
            <p><strong>The ScalebuildAI Team</strong></p>
        </div>
    </div>
</body>
</html>
                """,
                "text_content": f"""
Welcome to ScalebuildAI!

Hello {kwargs.get('name', 'there')}!

We're thrilled to have you join the ScalebuildAI community! Your account has been successfully created with the email address: {to_email}

Get started with our powerful AI features:
• AI-Powered Presentations - Create stunning presentations in minutes
• Logo Generation - Design professional logos with AI  
• Document Creation - Generate comprehensive business documents
• Short Video Generation - Create engaging video content

Ready to transform your business with AI? Visit: https://scalebuild-new.vercel.app/dashboard

If you have any questions, our support team is here to help!

Best regards,
The ScalebuildAI Team
                """
            },
            "contact": {
                "subject": f"New Contact Form Message from {kwargs.get('sender_name', 'User')}",
                "html_content": f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form Message</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; padding: 20px 0; border-bottom: 2px solid #28a745; }}
        .header h1 {{ color: #28a745; margin: 0; }}
        .message-details {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .detail-row {{ margin: 15px 0; padding: 10px; background-color: #ffffff; border-left: 4px solid #28a745; }}
        .message-content {{ background-color: #ffffff; padding: 20px; border: 1px solid #ddd; border-radius: 5px; margin: 15px 0; }}
        .footer {{ text-align: center; padding: 20px 0; border-top: 1px solid #eee; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📧 New Contact Form Message</h1>
        </div>
        
        <div class="message-details">
            <h3>Message Details:</h3>
            <div class="detail-row">
                <strong>From:</strong> {kwargs.get('sender_name', 'Unknown')}
            </div>
            <div class="detail-row">
                <strong>Email:</strong> {kwargs.get('sender_email', 'Unknown')}
            </div>
            <div class="detail-row">
                <strong>Subject:</strong> {kwargs.get('subject', 'No subject')}
            </div>
            
            <div class="message-content">
                <h4>Message:</h4>
                <p>{kwargs.get('message', 'No message content')}</p>
            </div>
        </div>
        
        <div class="footer">
            <p><em>This message was sent through the ScalebuildAI contact form.</em></p>
        </div>
    </div>
</body>
</html>
                """,
                "text_content": f"""
New Contact Form Message

Message Details:
From: {kwargs.get('sender_name', 'Unknown')}
Email: {kwargs.get('sender_email', 'Unknown')}
Subject: {kwargs.get('subject', 'No subject')}

Message:
{kwargs.get('message', 'No message content')}

---
This message was sent through the ScalebuildAI contact form.
                """
            },
            "password_reset": {
                "subject": "Reset Your ScalebuildAI Password 🔐",
                "html_content": f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; padding: 20px 0; border-bottom: 2px solid #dc3545; }}
        .header h1 {{ color: #dc3545; margin: 0; }}
        .content {{ padding: 30px 0; }}
        .reset-info {{ background-color: #fff3cd; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107; }}
        .btn {{ display: inline-block; padding: 12px 24px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px 0; border-top: 1px solid #eee; color: #666; }}
        .warning {{ color: #856404; background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Password Reset Request</h1>
        </div>
        
        <div class="content">
            <h2>Hello {kwargs.get('name', 'there')}!</h2>
            
            <p>We received a request to reset your password for your ScalebuildAI account.</p>
            
            <div class="reset-info">
                <p><strong>Reset Token:</strong> {kwargs.get('reset_token', 'TOKEN_NOT_PROVIDED')}</p>
                <p><strong>This token expires in:</strong> 1 hour</p>
            </div>
            
       
        </div>
        
        <div class="footer">
            <p>For security reasons, this link will expire in 1 hour.</p>
            <p><strong>The ScalebuildAI Team</strong></p>
        </div>
    </div>
</body>
</html>
                """,
                "text_content": f"""
Password Reset Request

Hello {kwargs.get('name', 'there')}!

We received a request to reset your password for your ScalebuildAI account.

Reset Token: {kwargs.get('reset_token', 'TOKEN_NOT_PROVIDED')}
This token expires in: 1 hour

Reset your password here: {kwargs.get('reset_url', 'URL_NOT_PROVIDED')}

SECURITY NOTICE:
If you didn't request this password reset, please ignore this email. Your password will remain unchanged.

For security reasons, this link will expire in 1 hour.

Best regards,
The ScalebuildAI Team
                """
            }
        }
        
        if template_type not in templates:
            raise HTTPException(
                status_code=400, 
                detail=f"Unknown email template: {template_type}. Available templates: {list(templates.keys())}"
            )
        
        template = templates[template_type]
        return self.send_email(
            to_email=to_email,
            subject=template["subject"],
            html_content=template["html_content"],
            text_content=template.get("text_content"),
            from_email=from_email,
            tags=[{"name": "template", "value": template_type}]
        )


# Global Resend email service instance
resend_email_service = ResendEmailService()