from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from post_scheduler.instagram.scheduler import run_scheduler
from contextlib import asynccontextmanager
import threading

from app.routers import templates, carousel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start scheduler in a background thread
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
    
    yield  # <-- This is required so the app runs after starting the thread

app = FastAPI(
    title="Instagram Content Automation",
    description="API for automating Instagram content generation",
    version="1.0.0",
    lifespan=lifespan
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