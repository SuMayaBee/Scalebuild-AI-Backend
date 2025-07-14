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

