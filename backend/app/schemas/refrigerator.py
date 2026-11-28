from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class RefrigeratorBase(BaseModel):
    name: str = "My Smart Refrigerator"
    model: Optional[str] = "Virtual SmartFridge AI v1"
    location: Optional[str] = "Kitchen"
    target_temperature_celsius: float = 3.5
    current_temperature_celsius: Optional[float] = 3.5


class RefrigeratorCreate(RefrigeratorBase):
    pass


class RefrigeratorUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    target_temperature_celsius: Optional[float] = None
    current_temperature_celsius: Optional[float] = None


class RefrigeratorResponse(RefrigeratorBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
