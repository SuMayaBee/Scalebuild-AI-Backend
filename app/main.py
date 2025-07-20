from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import router as auth_router
from app.presentation.routes import router as presentation_router

app = FastAPI()

# Allow CORS for Next.js frontend on port 3000 and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://ai-digital-business-builder.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(presentation_router, prefix="/presentation", tags=["presentation"])
