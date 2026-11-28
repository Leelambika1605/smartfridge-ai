from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.session import Base


class Refrigerator(Base):
    __tablename__ = "refrigerators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), default="My Smart Refrigerator", nullable=False)
    model = Column(String(100), default="Virtual SmartFridge AI v1", nullable=True)
    location = Column(String(100), default="Kitchen", nullable=True)
    target_temperature_celsius = Column(Float, default=3.5, nullable=False)
    current_temperature_celsius = Column(Float, default=3.5, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    owner = relationship("User", back_populates="refrigerators")
