# 📧 Resend Email Service - ScalebuildAI

Simple email sending service using Resend API for the ScalebuildAI platform.

## 🚀 Quick Setup

### 1. Environment Configuration

Add these variables to your `.env` file:

```env
RESEND_API_KEY=re_your_api_key_here
SENDER_EMAIL=noreply@scalebuild.ai
SENDER_NAME=ScalebuildAI
```

### 2. DNS Configuration

Add these DNS records to your `scalebuild.ai` domain:

```
Type: MX
Name: send
Priority: 10
Value: feedback-smtp.us-east-1.amazonses.com

Type: TXT
Name: send
Value: v=spf1 include:amazonses.com ~all

Type: TXT
Name: resend._domainkey
Value: p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC... (from Resend dashboard)

Type: TXT
Name: _dmarc
Value: v=DMARC1; p=none;
```

## 📧 API Endpoint

**Endpoint:** `POST /resend/send`  
**Authentication:** ❌ Not Required  
**Base URL:** `http://localhost:8000`

### Request Body

#### Minimal Request (Required Fields Only)
```json
{
  "to_email": "recipient@example.com",
  "subject": "Your Email Subject",
  "html_content": "<h1>Hello!</h1><p>Your email content here</p>"
}
```

#### Full Request (All Fields)
```json
{
  "to_email": "recipient@example.com",
  "subject": "Your Email Subject",
  "html_content": "<h1>Hello!</h1><p>Your email content here</p>",
  "text_content": "Hello! Your email content here",
  "from_email": "custom@scalebuild.ai",
  "reply_to": "support@scalebuild.ai",
  "tags": [
    {"name": "category", "value": "notification"},
    {"name": "campaign", "value": "welcome"}
  ]
}
```

### Response

#### Success Response
```json
{
  "success": true,
  "message": "Email sent successfully via Resend",
  "recipient": "recipient@example.com",
  "email_id": "95f803b9-079a-4d65-b276-6a16c9136f64",
  "data": {
    "id": "95f803b9-079a-4d65-b276-6a16c9136f64"
  }
}
```

#### Error Response
```json
{
  "detail": "Resend email service error: [error message]"
}
```

## 🔧 Usage Examples

### cURL Command
```bash
curl -X POST "http://localhost:8000/resend/send" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "user@example.com",
    "subject": "Hello from ScalebuildAI",
    "html_content": "<h1>Welcome!</h1><p>Thank you for joining ScalebuildAI.</p>"
  }'
```

### Python Example
```python
import httpx
import asyncio

async def send_email():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/resend/send",
            json={
                "to_email": "user@example.com",
                "subject": "Hello from ScalebuildAI",
                "html_content": "<h1>Welcome!</h1><p>Thank you for joining ScalebuildAI.</p>"
            }
        )
        print(response.json())

asyncio.run(send_email())
```

### JavaScript/Node.js Example
```javascript
const response = await fetch('http://localhost:8000/resend/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    to_email: 'user@example.com',
    subject: 'Hello from ScalebuildAI',
    html_content: '<h1>Welcome!</h1><p>Thank you for joining ScalebuildAI.</p>'
  })
});

const result = await response.json();
console.log(result);
```

## 📋 Field Specifications

### Required Fields
- **to_email** (string): Valid email address of recipient
- **subject** (string): Email subject line (1-200 characters)
- **html_content** (string): Email body in HTML format

### Optional Fields
- **text_content** (string): Plain text version of email
- **from_email** (string): Custom sender email (must be from verified domain)
- **reply_to** (string): Reply-to email address
- **tags** (array): List of key-value pairs for email tracking

## 🚨 Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `API key not configured` | Missing RESEND_API_KEY | Add API key to .env file |
| `Invalid sender domain` | Using unverified domain | Use @scalebuild.ai emails only |
| `Invalid email format` | Malformed email address | Check email format |
| `DNS not configured` | Domain not verified | Complete DNS setup |

## ✅ Testing

### Test the Service
```bash
curl -X POST "http://localhost:8000/resend/send" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "your-email@example.com",
    "subject": "Test Email",
    "html_content": "<h1>Test</h1><p>This is a test email.</p>"
  }'
```

### Expected Success Response
```json
{
  "success": true,
  "message": "Email sent successfully via Resend",
  "recipient": "your-email@example.com",
  "email_id": "95f803b9-079a-4d65-b276-6a16c9136f64",
  "data": {
    "id": "95f803b9-079a-4d65-b276-6a16c9136f64"
  }
}
```

## 🔍 Troubleshooting

1. **Check server logs** for detailed error messages
2. **Verify DNS records** are properly configured
3. **Confirm domain verification** in Resend dashboard
4. **Test with minimal request** first
5. **Restart FastAPI server** after .env changes

## 📚 Resources

- [Resend Documentation](https://resend.com/docs)
- [DNS Setup Guide](https://resend.com/docs/send-with-domains)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**✨ Ready to send emails!** The service is now configured and ready to use with your `scalebuild.ai` domain.