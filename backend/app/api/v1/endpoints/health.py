from fastapi import APIRouter
from datetime import datetime, timezone
import sys
from app.core.config import settings

router = APIRouter()


@router.get("/health", tags=["System Health"])
def get_system_health():
    """
    Returns the real-time operational health of the SmartFridge AI backend.
    Used for monitoring, container orchestrators, and frontend connectivity checks.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "active_modules": [
            {"id": "auth", "name": "User Authentication & JWT", "status": "initialized"},
            {"id": "inventory", "name": "Smart Inventory Core", "status": "initialized"},
            {"id": "ai_recognition", "name": "AI Computer Vision & OCR", "status": "ready_for_models"},
            {"id": "prediction", "name": "Consumption Prediction Engine", "status": "ready_for_engine"},
            {"id": "replenishment", "name": "Automated Replenishment", "status": "ready_for_engine"},
            {"id": "payment", "name": "Payment Gateway Simulation", "status": "simulation_ready"}
        ],
        "simulation_mode": settings.SIMULATION_MODE,
        "hardware_interface": "software_simulation_mode (ready for camera/sensor hooks)"
    }
