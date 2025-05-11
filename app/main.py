from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import templates, carousel

app = FastAPI(
    title="Instagram Content Automation",
    description="API for automating Instagram content generation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(templates.router, prefix="/api/v1", tags=["templates"])
app.include_router(carousel.router, prefix="/api/v1", tags=["carousel"])