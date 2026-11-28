from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class InventoryItem(BaseModel):
    id: str
    name: str
    category: str # "Groceries", "Beverages", "Medicines", "Skincare", "Prepared Food", "Other"
    quantity: float
    unit: str # "pcs", "liters", "bottles", "grams", "containers"
    capacity: float # Total container capacity for % tracking
    stock_percent: int # 0 to 100
    expiry_date: str # YYYY-MM-DD
    shelf_location: str # e.g. "Top Shelf", "Door Bin 1", "Crisper Drawer", "Medicine Box"
    temperature_target_min: float # °C
    temperature_target_max: float # °C
    price: float # Estimated reorder cost in USD
    auto_reorder_enabled: bool = True
    requires_approval: bool = False # Medicines or expensive items require confirmation
    days_until_expiry: Optional[int] = None
    status: Optional[str] = None # "Optimal", "Low Stock", "Expiring Soon", "Expired", "Temp Alert"
    consumption_rate_per_day: float = 0.2

class InventoryCreate(BaseModel):
    name: str
    category: str
    quantity: float
    unit: str
    capacity: float
    expiry_date: str
    shelf_location: str
    temperature_target_min: float = 2.0
    temperature_target_max: float = 8.0
    price: float = 5.0
    auto_reorder_enabled: bool = True
    requires_approval: bool = False

class FridgeStatus(BaseModel):
    temperature: float # Current internal temperature in °C
    humidity: float # Current humidity %
    door_state: str # "Closed" or "Open"
    door_open_count_today: int
    cooling_health: str # "Optimal", "High Temp Alert", "Sensor Malfunction"
    last_door_cycle: str
    last_camera_sync: str

class ReorderItem(BaseModel):
    id: str
    item_id: str
    item_name: str
    category: str
    quantity_to_order: float
    unit: str
    estimated_cost: float
    status: str # "Pending Approval", "Approved & Placed", "In Transit", "Delivered"
    created_at: str
    supplier: str = "Instacart QuickFresh"
    requires_approval: bool = False

class SettingsConfig(BaseModel):
    monthly_budget: float = 250.0
    spent_this_month: float = 64.50
    auto_pay_enabled: bool = True
    approval_threshold_price: float = 25.0 # Items above this price need manual approval
    target_fridge_temp: float = 3.8
    temp_alert_threshold: float = 7.5
    categories_auto_reorder: List[str] = [
        "Groceries", "Beverages", "Skincare", "Prepared Food"
    ]
    sms_alerts_enabled: bool = True
    push_notifications: bool = True

class DoorSimulationRequest(BaseModel):
    action: str # "add_item", "remove_item", "consume_item", "door_cycle"
    item_name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[float] = None
