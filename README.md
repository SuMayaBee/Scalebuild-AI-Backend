# ScalebuildAI Backend

This is the FastAPI backend for ScalebuildAI, using SQLAlchemy ORM and NeonDB (Postgres) with Alembic migrations.

## Setup Instructions

1. **Clone the repository and navigate to the backend folder:**
   ```bash
   git clone <your-repo-url>
   cd Backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Create a `.env` file in the `Backend` directory:
     ```env
     DATABASE_URL=postgresql://<user>:<password>@<host>/<db>?sslmode=require&channel_binding=require
     SECRET_KEY=your_secret_key_here
     ```

5. **Run Alembic migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API docs:**
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

---

## Authentication Endpoints

### 1. Signup
- **POST** `/auth/signup`
- **Request Body (JSON):**
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "is_active": true
  }
  ```

### 2. Signin
- **POST** `/auth/signin`
- **Request Body (JSON):**
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "access_token": "<jwt_token>",
    "token_type": "bearer"
  }
  ```

### 3. Forgot Password
- **POST** `/auth/forgot-password`
- **Request Body (JSON):**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "msg": "Password reset token generated",
    "token": "<reset_token>"
  }
  ```

### 4. Reset Password
- **POST** `/auth/reset-password`
- **Request Body (JSON):**
  ```json
  {
    "token": "<reset_token>",
    "new_password": "yournewpassword"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "msg": "Password reset successful"
  }
  ```

---

## Presentation Endpoints

### 1. Generate Presentation Outline
- **POST** `/presentation/outline`
- **Request Body (JSON):**
  ```json
  {
    "prompt": "AI for business",
    "numberOfCards": 5,
    "language": "English"
  }
  ```
- **Response:**
  Streamed plain text outline.

### 2. Generate Presentation Slides
- **POST** `/presentation/generate`
- **Request Body (JSON):**
  ```json
  {
    "title": "AI in Business",
    "outline": [
      "Introduction to AI in Business",
      "Types of AI Applications in Business",
      "Enhancing Decision-Making with AI",
      "AI and Customer Experience",
      "Ethical Considerations and Future of AI in Business"
    ],
    "language": "English",
    "tone": "Professional"
  }
  ```
- **Response:**
  Streamed XML (application/xml).

### 3. Create Presentation
- **POST** `/presentation/create`
- **Request Body (JSON):**
  ```json
  {
    "title": "AI in Business",
    "content": {
      "xml": "<PRESENTATION>...</PRESENTATION>"
    },
    "theme": "default",
    "language": "English",
    "tone": "Professional",
    "user_id": 1
  }
  ```
- **Response (JSON):**
  ```json
  {
    "id": "1",
    "title": "AI in Business",
    "content": {
      "xml": "<PRESENTATION>...</PRESENTATION>"
    },
    "theme": "default",
    "language": "English",
    "tone": "Professional",
    "userId": "1",
    "createdAt": "2025-07-15T12:00:00Z",
    "updatedAt": "2025-07-15T12:00:00Z",
    "isPublic": false,
    "slug": null
  }
  ```

### 4. Get Presentation by ID
- **GET** `/presentation/{presentation_id}`
- **Response:** Same as above.

### 5. Update Presentation
- **PUT** `/presentation/{presentation_id}`
- **Request Body (JSON):**
  ```json
  {
    "content": {
      "xml": "<PRESENTATION>...</PRESENTATION>"
    },
    "title": "AI in Business - Updated"
  }
  ```
- **Response:** Same as above.

### 6. Get All Presentations for a User
- **GET** `/presentation/user/{user_email}`
- **Response:**
  ```json
  [
    {
      "id": "1",
      "title": "AI in Business",
      "content": {
        "xml": "<PRESENTATION>...</PRESENTATION>"
      },
      "theme": "default",
      "language": "English",
      "tone": "Professional",
      "userId": "1",
      "createdAt": "2025-07-15T12:00:00Z",
      "updatedAt": "2025-07-15T12:00:00Z",
      "isPublic": false,
      "slug": null
    }
  ]
  ```

### 7. Delete Presentation
- **DELETE** `/presentation/{presentation_id}`
- **Response (JSON):**
  ```json
  { "message": "Presentation deleted successfully" }
  ```

### 8. Generate Image for Presentation
- **POST** `/presentation/generate-image`
- **Request Body (JSON):**
  ```json
  {
    "prompt": "aerial view of solar panels and wind turbines working harmoniously in a green landscape",
    "size": "1024x1024"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "success": true,
    "url": "https://storage.googleapis.com/deck123/presentation_images/aerial_view_of_solar_panels_and_wind_turbines_working_harmoniously_in_a_green_landscape.png",
    "prompt": "aerial view of solar panels and wind turbines working harmoniously in a green landscape",
    "model": "dall-e-3",
    "size": "1024x1024",
    "quality": null,
    "filename": null,
    "error": null
  }
  ```

### 9. Get User Images
- **GET** `/presentation/images/{user_email}`
- **Response (JSON):**
  ```json
  [
    {
      "id": "img1",
      "url": "https://your-bucket/image.png",
      "prompt": "A futuristic business meeting",
      "model": "dall-e-3",
      "size": "1024x1024",
      "quality": "hd",
      "filename": "image.png",
      "userId": "1",
      "createdAt": "2025-07-15T12:00:00Z"
    }
  ]
  ```

### 10. Get Image Info by URL
- **GET** `/presentation/image-info?url=https://your-bucket/image.png`
- **Response (JSON):**
  ```json
  {
    "id": "img1",
    "url": "https://your-bucket/image.png",
    "prompt": "A futuristic business meeting",
    "model": "dall-e-3",
    "size": "1024x1024",
    "quality": "hd",
    "filename": "image.png",
    "userId": "1",
    "createdAt": "2025-07-15T12:00:00Z"
  }
  ```

### 11. Generate Image for Presentation (with Presentation ID)
- **POST** `/presentation/generate-image`
- **Request Body (JSON):**
  ```json
  {
    "prompt": "A beautiful sunset over mountains",
    "presentation_id": 123,
    "size": "1024x1024"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "success": true,
    "url": "https://storage.googleapis.com/deck123/a_beautiful_sunset_over_mountains.png",
    "prompt": "A beautiful sunset over mountains",
    "model": "dall-e-3",
    "size": "1024x1024",
    "filename": "a_beautiful_sunset_over_mountains.png",
    "error": null
  }
  ```

### 12. Get All Images for a Presentation
- **GET** `/presentation/{presentation_id}/images`
- **Response (JSON):**
  ```json
  [
    {
      "id": 1,
      "presentation_id": 123,
      "image_url": "https://storage.googleapis.com/deck123/sunset_mountains.png",
      "prompt": "A beautiful sunset over mountains",
      "filename": "sunset_mountains.png",
      "model": "dall-e-3",
      "size": "1024x1024",
      "created_at": "2025-07-20T21:30:00Z"
    }
  ]
  ```

---

## Logo Endpoints

### 1. Generate Logo and Save to Database
- **POST** `/logo/design`
- **Request Body (JSON):**
  ```json
  {
    "logo_title": "TechFlow Solutions",
    "logo_vision": "A modern tech company that helps businesses streamline their digital workflows",
    "color_palette_name": "Neon Pop",
    "logo_style": "Modern Sharp Lined Logos",
    "user_id": 123
  }
  ```
- **Response (JSON):**
  ```json
  {
    "id": 1,
    "user_id": 123,
    "logo_image_url": "https://storage.googleapis.com/deck123/logo_TechFlow_Solutions.png",
    "remove_bg_logo_image_url": null,
    "content": {
      "design_specification": {
        "logo_overview": {
          "title": "TechFlow Solutions",
          "concept": "Brief description of the main logo concept",
          "target_audience": "Who this logo is designed for",
          "brand_message": "What message the logo communicates"
        }
      },
      "generation_type": "structured",
      "enhanced_prompt": "...",
      "image_model": "dall-e-3"
    },
    "logo_title": "TechFlow Solutions",
    "logo_vision": "A modern tech company that helps businesses streamline their digital workflows",
    "color_palette_name": "Neon Pop",
    "logo_style": "Modern Sharp Lined Logos",
    "created_at": "2025-07-20T21:30:00Z",
    "updated_at": "2025-07-20T21:30:00Z"
  }
  ```

### 2. Remove Background from Logo
- **POST** `/logo/remove_bg`
- **Request Body (JSON):**
  ```json
  {
    "logo_id": 1
  }
  ```
- **Response (JSON):**
  ```json
  {
    "success": true,
    "logo_id": 1,
    "remove_bg_logo_image_url": "https://storage.googleapis.com/deck123/no_bg_logo_TechFlow_Solutions.png",
    "error": null
  }
  ```

### 3. Get Logo by ID
- **GET** `/logo/{logo_id}`
- **Response (JSON):**
  ```json
  {
    "id": 1,
    "user_id": 123,
    "logo_image_url": "https://storage.googleapis.com/deck123/logo_TechFlow_Solutions.png",
    "remove_bg_logo_image_url": "https://storage.googleapis.com/deck123/no_bg_logo_TechFlow_Solutions.png",
    "content": {
      "design_specification": {...},
      "generation_type": "structured",
      "enhanced_prompt": "...",
      "image_model": "dall-e-3"
    },
    "logo_title": "TechFlow Solutions",
    "logo_vision": "A modern tech company that helps businesses streamline their digital workflows",
    "color_palette_name": "Neon Pop",
    "logo_style": "Modern Sharp Lined Logos",
    "created_at": "2025-07-20T21:30:00Z",
    "updated_at": "2025-07-20T21:30:00Z"
  }
  ```

### 4. Get All Logos for a User
- **GET** `/logo/user/{user_id}`
- **Response (JSON):**
  ```json
  [
    {
      "id": 1,
      "user_id": 123,
      "logo_image_url": "https://storage.googleapis.com/deck123/logo_TechFlow_Solutions.png",
      "remove_bg_logo_image_url": "https://storage.googleapis.com/deck123/no_bg_logo_TechFlow_Solutions.png",
      "content": {...},
      "logo_title": "TechFlow Solutions",
      "logo_vision": "A modern tech company that helps businesses streamline their digital workflows",
      "color_palette_name": "Neon Pop",
      "logo_style": "Modern Sharp Lined Logos",
      "created_at": "2025-07-20T21:30:00Z",
      "updated_at": "2025-07-20T21:30:00Z"
    }
  ]
  ```

### 5. Delete Logo
- **DELETE** `/logo/{logo_id}`
- **Response (JSON):**
  ```json
  {
    "message": "Logo deleted successfully"
  }
  ```

### 6. Generate Logo Design Only (No Database Save)
- **POST** `/logo/design-only`
- **Request Body (JSON):**
  ```json
  {
    "logo_title": "TechFlow Solutions",
    "logo_vision": "A modern tech company that helps businesses streamline their digital workflows",
    "color_palette_name": "Neon Pop",
    "logo_style": "Modern Sharp Lined Logos",
    "user_id": 123
  }
  ```
- **Response (JSON):**
  ```json
  {
    "design_specification": {
      "logo_overview": {
        "title": "TechFlow Solutions",
        "concept": "Brief description of the main logo concept",
        "target_audience": "Who this logo is designed for",
        "brand_message": "What message the logo communicates"
      }
    },
    "raw_specification": "...",
    "logo_title": "TechFlow Solutions",
    "generation_type": "structured"
  }
  ```

---

## Logo Configuration Options

### Available Color Palettes:
- **"Neon Pop"**: `["#FF0000", "#00FF00", "#D500FF", "#FF00FF", "#F6FF00"]`
- **"Deep Dusk"**: `["#112266", "#3A176A", "#782AB6", "#B51FA7", "#F70072"]`
- **"Sunset Sorbet"**: `["#FF2350", "#FF5D2A", "#FF9945", "#FFB347", "#FFE156"]`
- **"Emerald City"**: `["#016A53", "#019267", "#01B087", "#00C9A7", "#16D5C7"]`
- **"Coffee Tones"**: `["#6A4E42", "#7E5C4C", "#9C6D59", "#B08B74", "#CDC1B5"]`
- **"Purple Parade"**: `["#5C258D", "#763AA6", "#A25BCF", "#C569E6", "#E159F8"]`

### Available Logo Styles:
- **"Cartoon Logo"**
- **"App Logo"**
- **"Modern Mascot Logos"**
- **"Black And White Line Logos"**
- **"Minimalists and Elegant Logos"**
- **"Vintage Custom Logos"**
- **"Modern Sharp Lined Logos"**

---

## Short Video Generation Endpoints

### 1. Generate Short Video
- **POST** `/short-video/generate`
- **Request Body (JSON):**
  ```json
  {
    "user_id": 123,
    "prompt": "A cat flying with colorful balloons in a sunny sky",
    "aspect_ratio": "16:9",
    "duration": "8",
    "audio_generation": true,
    "watermark": true,
    "person_generation": "allow_all"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "id": 1,
    "user_id": 123,
    "prompt": "A cat flying with colorful balloons in a sunny sky",
    "video_url": "https://storage.googleapis.com/deck123/short_video_cat_flying_a1b2c3d4.mp4",
    "aspect_ratio": "16:9",
    "duration": "8",
    "audio_generation": true,
    "watermark": true,
    "person_generation": "allow_all",
    "created_at": "2025-07-21T06:20:00Z",
    "updated_at": "2025-07-21T06:20:00Z"
  }
  ```

### 2. Get Short Video by ID
- **GET** `/short-video/{video_id}`
- **Response:** Same as above

### 3. Get All Short Videos for User
- **GET** `/short-video/user/{user_id}`
- **Response:**
  ```json
  [
    {
      "id": 1,
      "user_id": 123,
      "prompt": "A cat flying with colorful balloons in a sunny sky",
      "video_url": "https://storage.googleapis.com/deck123/short_video_cat_flying_a1b2c3d4.mp4",
      "aspect_ratio": "16:9",
      "duration": "8",
      "audio_generation": true,
      "watermark": true,
      "person_generation": "allow_all",
      "created_at": "2025-07-21T06:20:00Z",
      "updated_at": "2025-07-21T06:20:00Z"
    }
  ]
  ```

### 4. Delete Short Video
- **DELETE** `/short-video/{video_id}`
- **Response (JSON):**
  ```json
  { "message": "Short video deleted successfully" }
  ```

### 5. Check Video Service Status
- **GET** `/short-video/status/check`
- **Response (JSON):**
  ```json
  {
    "status": "healthy",
    "service": "Veo 3.0 Video Generation",
    "model": "veo-3.0-generate-preview",
    "available_options": {
      "aspect_ratios": ["16:9", "9:16", "1:1"],
      "durations": ["4", "8"],
      "person_generation": ["allow_all", "allow_none", "allow_some"]
    }
  }
  ```

---

## Document Generation Endpoints

### 1. Business Proposal
- **POST** `/documents/business-proposal`
- **Request Body (JSON):**
  ```json
  {
    "user_id": 123,
    "company_name": "TechFlow Solutions",
    "client_name": "ABC Corporation",
    "project_title": "Website Redesign Project",
    "project_description": "Complete website overhaul with modern design and improved user experience",
    "services_offered": [
      "Web Design",
      "Frontend Development", 
      "Backend Development",
      "SEO Optimization",
      "Content Management System"
    ],
    "timeline": "3 months",
    "budget_range": "$15,000 - $25,000",
    "contact_person": "John Smith",
    "contact_email": "john@techflow.com",
    "logo_url": "https://storage.googleapis.com/deck123/company_logo.png"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "id": 1,
    "user_id": 123,
    "company_name": "TechFlow Solutions",
    "client_name": "ABC Corporation",
    "project_title": "Website Redesign Project",
    "ai_generated_content": "BUSINESS PROPOSAL\n\nExecutive Summary\n\nThis proposal outlines a comprehensive website redesign project...",
    "input_data": { /* Original request data */ },
    "docs_url": null,
    "created_at": "2025-07-21T06:30:00Z",
    "updated_at": "2025-07-21T06:30:00Z"
  }
  ```

### 2. Partnership Agreement
- **POST** `/documents/partnership-agreement`
- **Request Body (JSON):**
  ```json
  {
    "user_id": 123,
    "party1_name": "TechFlow Solutions LLC",
    "party1_address": "123 Business Ave, Tech City, TC 12345",
    "party2_name": "Digital Marketing Pro Inc",
    "party2_address": "456 Commerce St, Marketing Town, MT 67890",
    "partnership_purpose": "Joint venture for providing comprehensive digital solutions to enterprise clients",
    "partnership_duration": "3 years",
    "profit_sharing_ratio": "60% TechFlow, 40% Digital Marketing Pro",
    "responsibilities_party1": [
      "Technical development and implementation",
      "Software architecture and design",
      "Quality assurance and testing",
      "Technical support and maintenance"
    ],
    "responsibilities_party2": [
      "Marketing strategy and campaigns",
      "Client acquisition and relationship management",
      "Brand development and promotion",
      "Social media management"
    ],
    "effective_date": "2025-02-01",
    "logo_url": "https://storage.googleapis.com/deck123/partnership_logo.png"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "id": 1,
    "user_id": 123,
    "party1_name": "TechFlow Solutions LLC",
    "party2_name": "Digital Marketing Pro Inc",
    "partnership_purpose": "Joint venture for providing comprehensive digital solutions to enterprise clients",
    "ai_generated_content": "PARTNERSHIP AGREEMENT\n\nThis Partnership Agreement is entered into...",
    "input_data": { /* Original request data */ },
    "docs_url": null,
    "created_at": "2025-07-21T06:30:00Z",
    "updated_at": "2025-07-21T06:30:00Z"
  }
  ```

### 3. Non-Disclosure Agreement (NDA)
- **POST** `/documents/nda`
- **Request Body (JSON):**
  ```json
  {
    "user_id": 123,
    "disclosing_party": "TechFlow Solutions LLC",
    "receiving_party": "ABC Corporation",
    "purpose": "Discussion of potential software development partnership and sharing of proprietary technology information",
    "confidential_info_description": "Technical specifications, source code, business strategies, client lists, financial information, and any proprietary methodologies",
    "duration": "5 years from the date of disclosure",
    "governing_law": "State of California",
    "effective_date": "2025-01-15",
    "logo_url": "https://storage.googleapis.com/deck123/nda_logo.png"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "id": 1,
    "user_id": 123,
    "disclosing_party": "TechFlow Solutions LLC",
    "receiving_party": "ABC Corporation",
    "purpose": "Discussion of potential software development partnership and sharing of proprietary technology information",
    "ai_generated_content": "NON-DISCLOSURE AGREEMENT\n\nThis Non-Disclosure Agreement is made between...",
    "input_data": { /* Original request data */ },
    "docs_url": null,
    "created_at": "2025-07-21T06:30:00Z",
    "updated_at": "2025-07-21T06:30:00Z"
  }
  ```

### 4. Contract
- **POST** `/documents/contract`
- **Request Body (JSON):**
  ```json
  {
    "user_id": 123,
    "contract_type": "service",
    "party1_name": "TechFlow Solutions LLC",
    "party1_address": "123 Business Ave, Tech City, TC 12345",
    "party2_name": "ABC Corporation",
    "party2_address": "789 Corporate Blvd, Business City, BC 54321",
    "service_description": "Custom web application development including frontend, backend, database design, and deployment",
    "contract_value": "$45,000",
    "payment_terms": "50% upfront, 30% at milestone completion, 20% upon final delivery",
    "duration": "6 months",
    "deliverables": [
      "Fully functional web application",
      "Source code and documentation",
      "User training materials",
      "3 months of technical support",
      "Deployment and hosting setup"
    ],
    "terms_conditions": [
      "All work must be completed within specified timeline",
      "Client approval required for major design changes",
      "Intellectual property rights transfer upon final payment",
      "Confidentiality of client data maintained",
      "Warranty period of 90 days for bug fixes"
    ],
    "effective_date": "2025-02-01",
    "logo_url": "https://storage.googleapis.com/deck123/contract_logo.png"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "id": 1,
    "user_id": 123,
    "contract_type": "service",
    "party1_name": "TechFlow Solutions LLC",
    "party2_name": "ABC Corporation",
    "service_description": "Custom web application development including frontend, backend, database design, and deployment",
    "ai_generated_content": "SERVICE CONTRACT\n\nThis Service Contract is entered into between...",
    "input_data": { /* Original request data */ },
    "docs_url": null,
    "created_at": "2025-07-21T06:30:00Z",
    "updated_at": "2025-07-21T06:30:00Z"
  }
  ```

### 5. Terms of Service
- **POST** `/documents/terms-of-service`
- **Request Body (JSON):**
  ```json
  {
    "user_id": 123,
    "company_name": "TechFlow Solutions",
    "website_url": "https://www.techflowsolutions.com",
    "company_address": "123 Business Ave, Tech City, TC 12345",
    "service_description": "Web development, software consulting, and digital transformation services for businesses",
    "user_responsibilities": [
      "Provide accurate information during registration",
      "Maintain confidentiality of account credentials",
      "Use services in compliance with applicable laws",
      "Respect intellectual property rights",
      "Report any security vulnerabilities promptly"
    ],
    "prohibited_activities": [
      "Unauthorized access to systems or data",
      "Distribution of malware or harmful code",
      "Harassment or abuse of other users",
      "Violation of intellectual property rights",
      "Use of services for illegal activities"
    ],
    "payment_terms": "Monthly subscription fees are due in advance. Late payments may result in service suspension.",
    "cancellation_policy": "Users may cancel their subscription at any time with 30 days written notice. No refunds for partial months.",
    "limitation_of_liability": "Company liability is limited to the amount paid for services in the preceding 12 months",
    "governing_law": "State of California",
    "contact_email": "legal@techflowsolutions.com",
    "logo_url": "https://storage.googleapis.com/deck123/tos_logo.png"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "id": 1,
    "user_id": 123,
    "company_name": "TechFlow Solutions",
    "website_url": "https://www.techflowsolutions.com",
    "service_description": "Web development, software consulting, and digital transformation services for businesses",
    "ai_generated_content": "TERMS OF SERVICE\n\nWelcome to TechFlow Solutions. These Terms of Service govern...",
    "input_data": { /* Original request data */ },
    "docs_url": null,
    "created_at": "2025-07-21T06:30:00Z",
    "updated_at": "2025-07-21T06:30:00Z"
  }
  ```

### 6. Privacy Policy
- **POST** `/documents/privacy-policy`
- **Request Body (JSON):**
  ```json
  {
    "user_id": 123,
    "company_name": "TechFlow Solutions",
    "website_url": "https://www.techflowsolutions.com",
    "company_address": "123 Business Ave, Tech City, TC 12345",
    "data_collected": [
      "Personal information (name, email, phone number)",
      "Account credentials and preferences",
      "Usage data and analytics",
      "Device information and IP addresses",
      "Cookies and tracking technologies"
    ],
    "data_usage_purpose": [
      "Provide and improve our services",
      "Process payments and transactions",
      "Send important notifications and updates",
      "Analyze usage patterns for optimization",
      "Comply with legal obligations"
    ],
    "third_party_sharing": "We do not sell personal data. We may share data with trusted service providers for business operations and as required by law.",
    "data_retention_period": "Personal data is retained for as long as necessary to provide services, typically 7 years for business records",
    "user_rights": [
      "Access your personal data",
      "Correct inaccurate information",
      "Delete your account and data",
      "Opt-out of marketing communications",
      "Data portability upon request"
    ],
    "cookies_usage": "We use essential cookies for functionality and analytics cookies to improve user experience. Users can manage cookie preferences in browser settings.",
    "contact_email": "privacy@techflowsolutions.com",
    "governing_law": "State of California and applicable federal laws",
    "effective_date": "2025-01-01",
    "logo_url": "https://storage.googleapis.com/deck123/privacy_logo.png"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "id": 1,
    "user_id": 123,
    "company_name": "TechFlow Solutions",
    "website_url": "https://www.techflowsolutions.com",
    "ai_generated_content": "PRIVACY POLICY\n\nEffective Date: January 1, 2025\n\nTechFlow Solutions is committed to protecting your privacy...",
    "input_data": { /* Original request data */ },
    "docs_url": null,
    "created_at": "2025-07-21T06:30:00Z",
    "updated_at": "2025-07-21T06:30:00Z"
  }
  ```

### Document Management Endpoints (Available for all document types)

#### Get Document by ID
- **GET** `/documents/{document_type}/{document_id}`
- **Example:** `GET /documents/business-proposal/1`

#### Get All Documents for User
- **GET** `/documents/{document_type}/user/{user_id}`
- **Example:** `GET /documents/business-proposal/user/123`

#### Update Document Content
- **PUT** `/documents/{document_type}/{document_id}`
- **Request Body (JSON):**
  ```json
  {
    "ai_generated_content": "Updated document content here..."
  }
  ```

#### Upload Document File
- **POST** `/documents/upload/{document_type}/{document_id}`
- **Content-Type:** `multipart/form-data`
- **Form Data:** `file` (DOCX, PDF, or other document file)
- **Response (JSON):**
  ```json
  {
    "success": true,
    "document_id": 1,
    "docs_url": "https://storage.googleapis.com/deck123/business_proposal_1_a1b2c3d4.docx",
    "error": null
  }
  ```

#### Get Available Document Types
- **GET** `/documents/types`
- **Response (JSON):**
  ```json
  {
    "document_types": [
      {
        "type": "business_proposal",
        "name": "Business Proposal",
        "description": "Comprehensive business proposals for client projects"
      },
      {
        "type": "partnership_agreement",
        "name": "Partnership Agreement",
        "description": "Legal partnership agreements between two parties"
      },
      {
        "type": "nda",
        "name": "Non-Disclosure Agreement",
        "description": "Confidentiality agreements to protect sensitive information"
      },
      {
        "type": "contract",
        "name": "Contract",
        "description": "Various types of contracts (service, employment, vendor)"
      },
      {
        "type": "terms_of_service",
        "name": "Terms of Service",
        "description": "Legal terms governing the use of websites and services"
      },
      {
        "type": "privacy_policy",
        "name": "Privacy Policy",
        "description": "Legal documents outlining data collection and privacy practices"
      }
    ]
  }
  ```

---

## API Summary

### Total Endpoints Available:
- **Authentication:** 4 endpoints
- **Presentations:** 12 endpoints
- **Logos:** 6 endpoints
- **Short Videos:** 5 endpoints
- **Document Generation:** 31 endpoints (6 types × 5 operations + 1 utility)

### **Total: 58+ API endpoints** for comprehensive AI-powered business tools!

### Key Features:
- ✅ **AI-Powered Content Generation** (GPT-4, DALL-E 3, Veo 3.0)
- ✅ **Database Persistence** (PostgreSQL with user associations)
- ✅ **Cloud Storage Integration** (Google Cloud Storage)
- ✅ **File Upload Support** (DOCX, PDF, images, videos)
- ✅ **Complete CRUD Operations** (Create, Read, Update, Delete)
- ✅ **User Management** (Authentication and user-specific data)
- ✅ **Professional Document Generation** (Legal and business documents)
- ✅ **Logo Design with Background Removal**
- ✅ **Presentation Creation with AI Images**
- ✅ **Short Video Generation** (Text-to-video AI)