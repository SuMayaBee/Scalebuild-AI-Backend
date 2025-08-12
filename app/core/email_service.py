"""
Email Service for sending emails
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List
from fastapi import HTTPException


class EmailService:
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.sender_name = os.getenv("SENDER_NAME", "ScalebuildAI")
        
        if not self.sender_email or not self.sender_password:
            print("⚠️ Warning: Email credentials not configured. Set SENDER_EMAIL and SENDER_PASSWORD in .env")
    
    def send_email(
        self, 
        to_email: str, 
        subject: str, 
        message: str, 
        html_message: Optional[str] = None,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """
        Send an email to the specified recipient.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            message: Plain text message
            html_message: Optional HTML message
            attachments: Optional list of file paths to attach
            
        Returns:
            bool: True if email sent successfully, False otherwise
            
        Raises:
            HTTPException: If email configuration is missing or sending fails
        """
        if not self.sender_email or not self.sender_password:
            raise HTTPException(
                status_code=500, 
                detail="Email service not configured. Please contact administrator."
            )
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text part
            text_part = MIMEText(message, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_message:
                html_part = MIMEText(html_message, 'html')
                msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    if os.path.isfile(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
            
            # Connect to server and send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable encryption
            server.login(self.sender_email, self.sender_password)
            
            text = msg.as_string()
            server.sendmail(self.sender_email, to_email, text)
            server.quit()
            
            print(f"✅ Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print(f"❌ SMTP Authentication failed. Check email credentials.")
            raise HTTPException(
                status_code=500, 
                detail="Email authentication failed. Please check email configuration."
            )
        except smtplib.SMTPRecipientsRefused:
            print(f"❌ Invalid recipient email: {to_email}")
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid recipient email address: {to_email}"
            )
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to send email: {str(e)}"
            )
    
    def send_template_email(self, to_email: str, template_type: str, **kwargs) -> bool:
        """
        Send a templated email.
        
        Args:
            to_email: Recipient email address
            template_type: Type of template (welcome, reset_password, etc.)
            **kwargs: Template variables
            
        Returns:
            bool: True if email sent successfully
        """
        templates = {
            "welcome": {
                "subject": "Welcome to ScalebuildAI!",
                "message": f"""
Hello {kwargs.get('name', 'User')},

Welcome to ScalebuildAI! We're excited to have you on board.

Your account has been successfully created with email: {to_email}

Get started by exploring our features:
- AI-powered presentations
- Logo generation
- Document creation
- Short video generation

If you have any questions, feel free to reach out to our support team.

Best regards,
The ScalebuildAI Team
                """,
                "html_message": f"""
<html>
<body>
    <h2>Welcome to ScalebuildAI!</h2>
    <p>Hello <strong>{kwargs.get('name', 'User')}</strong>,</p>
    
    <p>Welcome to ScalebuildAI! We're excited to have you on board.</p>
    
    <p>Your account has been successfully created with email: <strong>{to_email}</strong></p>
    
    <h3>Get started by exploring our features:</h3>
    <ul>
        <li>🎨 AI-powered presentations</li>
        <li>🎯 Logo generation</li>
        <li>📄 Document creation</li>
        <li>🎬 Short video generation</li>
    </ul>
    
    <p>If you have any questions, feel free to reach out to our support team.</p>
    
    <p>Best regards,<br>
    <strong>The ScalebuildAI Team</strong></p>
</body>
</html>
                """
            },
            "contact": {
                "subject": f"Message from {kwargs.get('sender_name', 'User')}",
                "message": f"""
You have received a new message through ScalebuildAI contact form.

From: {kwargs.get('sender_name', 'Unknown')} ({kwargs.get('sender_email', 'Unknown')})
Subject: {kwargs.get('subject', 'No subject')}

Message:
{kwargs.get('message', 'No message content')}

---
This message was sent through ScalebuildAI contact form.
                """,
                "html_message": f"""
<html>
<body>
    <h2>New Contact Form Message</h2>
    <p>You have received a new message through ScalebuildAI contact form.</p>
    
    <table border="1" cellpadding="10" cellspacing="0">
        <tr>
            <td><strong>From:</strong></td>
            <td>{kwargs.get('sender_name', 'Unknown')} ({kwargs.get('sender_email', 'Unknown')})</td>
        </tr>
        <tr>
            <td><strong>Subject:</strong></td>
            <td>{kwargs.get('subject', 'No subject')}</td>
        </tr>
        <tr>
            <td><strong>Message:</strong></td>
            <td>{kwargs.get('message', 'No message content')}</td>
        </tr>
    </table>
    
    <p><em>This message was sent through ScalebuildAI contact form.</em></p>
</body>
</html>
                """
            }
        }
        
        if template_type not in templates:
            raise HTTPException(
                status_code=400, 
                detail=f"Unknown email template: {template_type}"
            )
        
        template = templates[template_type]
        return self.send_email(
            to_email=to_email,
            subject=template["subject"],
            message=template["message"],
            html_message=template.get("html_message")
        )


# Global email service instance
email_service = EmailService()