from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import router as auth_router
from app.presentation.routes import router as presentation_router
from app.logo.routes import router as logo_router
from app.document_generation.routes import router as document_router
from app.short_video.routes import router as short_video_router
from app.gcs.routes import router as gcs_router

app = FastAPI()

# Allow CORS for Next.js frontend on port 3000 and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://ai-digital-business-builder.vercel.app", "https://scalebuild-new.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(presentation_router, prefix="/presentation", tags=["presentation"])
app.include_router(logo_router, tags=["logo"])
app.include_router(document_router, tags=["documents"])
app.include_router(short_video_router, tags=["short-video"])
app.include_router(gcs_router, prefix="/gcs", tags=["gcs"])


# Market Research
# Competitor Analysis
# Perform the latest and uptodate market research for this <industry>
# perform the competitor analysis for this <company>
