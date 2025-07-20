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

