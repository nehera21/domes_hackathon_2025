"""
Main entry point for the FastAPI application.
Starts the uvicorn server and configures the app.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from settings import get_settings
from dependencies import get_databridge
from routers import users, projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events for the application.
    Handles startup and shutdown tasks.
    """
    # Startup
    settings = get_settings()
    print(f"🚀 Starting {settings.app_name} ({settings.api_version})")
    
    # Note: Database connection will be established on first query
    # Uncomment below to connect immediately on startup:
    # db = get_databridge()
    # await db.connect()
    
    yield
    
    # Shutdown
    db = get_databridge()
    await db.disconnect()
    print("👋 Application shutdown complete")


# Create FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.api_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


def start():
    """Start the uvicorn server"""
    settings = get_settings()
    uvicorn.run(
        "__main__:app",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    start()

