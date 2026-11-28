from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import logging
from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import engine, Base
import app.models  # Ensures all models are registered with Base.metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smartfridge")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure upload directories and create database tables if they don't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database tables: {e}")
    yield
    # Shutdown logic if any
    pass


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## SmartFridge AI Backend
    Intelligent Refrigerator Monitoring & Automated Replenishment System.
    
    ### Core Capabilities:
    * **User & Refrigerator Multi-tenancy**
    * **Computer Vision Item Recognition**
    * **Inventory Tracking & Expiry Schedules**
    * **Usage Pattern Learning & Predictive Depletion**
    * **Autonomous Replenishment & Simulated Payments**
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for uploads (refrigerator images, receipts)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Mount API Routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def root_status():
    """Root welcome endpoint providing API index and documentation link."""
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs_url": f"{settings.API_V1_STR}/docs",
        "health_check": f"{settings.API_V1_STR}/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
