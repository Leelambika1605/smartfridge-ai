from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, date, timedelta
import random

from models import (
    InventoryItem, InventoryCreate, FridgeStatus, ReorderItem,
    SettingsConfig, DoorSimulationRequest
)
from database import db

app = FastAPI(
    title="SmartFridge AI - Core Monitoring & Replenishment API",
    description="Universal AI Refrigerator System API powering inventory tracking, OCR expiry detection, multi-category management, and automated replenishment.",
    version="1.0.0"
)

# Enable CORS for local and hosted frontends (Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "system": "SmartFridge AI Backend",
        "status": "Operational",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# --- FRIDGE SENSORS & SYSTEM STATUS ---

@app.get("/api/status", response_model=FridgeStatus)
def get_fridge_status():
    # Simulate slight realistic temperature jitter between 3.4°C and 4.1°C
    db.status.temperature = round(3.6 + random.uniform(-0.3, 0.4), 1)
    db.status.humidity = round(57.5 + random.uniform(-1.5, 2.0), 1)
    return db.status

# --- DIGITAL INVENTORY CRUD ---

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory(category: Optional[str] = None, search: Optional[str] = None):
    items = db.get_all_items()
    if category and category != "All":
        items = [i for i in items if i.category.lower() == category.lower()]
    if search:
        s = search.lower()
        items = [i for i in items if s in i.name.lower() or s in i.shelf_location.lower()]
    return items

@app.post("/api/inventory", response_model=InventoryItem)
def create_inventory_item(item_in: InventoryCreate):
    return db.add_item(item_in.model_dump())

@app.get("/api/inventory/{item_id}", response_model=InventoryItem)
def get_single_item(item_id: str):
    item = db.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/api/inventory/{item_id}")
def delete_inventory_item(item_id: str):
    success = db.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Item {item_id} removed from inventory"}

@app.patch("/api/inventory/{item_id}/adjust")
def adjust_quantity(item_id: str, new_quantity: float = Query(..., ge=0)):
    updated = db.update_item_quantity(item_id, new_quantity)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

# --- AI CAMERA & DOOR CYCLE SIMULATION ---

@app.get("/api/camera/vision-feed")
def get_vision_feed():
    """Provides camera status and simulated bounding box detections for the dashboard UI."""
    return {
        "camera_status": "Online (HD 1080p Ultra-Wide 140°)",
        "last_frame_analyzed": db.status.last_camera_sync,
        "detection_engine": "YOLOv11-Universal + Multi-Modal Expiry OCR",
        "tracked_zones": ["Top Shelf", "Middle Shelf", "Bottom Shelf", "Door Bins", "Medicine Lockbox"],
        "active_bounding_boxes": [
            {"id": "box_1", "label": "Organic Whole Milk", "category": "Groceries", "confidence": 0.98, "shelf": "Door Bin 1", "level": "25%"},
            {"id": "box_2", "label": "Insulin Glargine Pen", "category": "Medicines", "confidence": 0.99, "shelf": "Medicine Lockbox Shelf", "level": "30%"},
            {"id": "box_3", "label": "Pasture Eggs", "category": "Groceries", "confidence": 0.95, "shelf": "Top Shelf", "level": "3/12 pcs"},
            {"id": "box_4", "label": "Cold-Pressed Juice", "category": "Beverages", "confidence": 0.97, "shelf": "Middle Shelf", "level": "80%"},
            {"id": "box_5", "label": "Retinol Serum", "category": "Skincare", "confidence": 0.94, "shelf": "Skincare Door Pocket", "level": "83%"}
        ]
    }

@app.post("/api/camera/simulate-door-event")
def simulate_door_event(req: DoorSimulationRequest):
    """
    Simulates the actual hardware workflow:
    1. Door opens -> Door closes
    2. Camera takes snapshot
    3. AI identifies change (Added, Removed, or Consumed)
    4. Inventory and auto-replenishment react instantly
    """
    db.status.door_state = "Closed"
    db.status.door_open_count_today += 1
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.status.last_door_cycle = now_str
    db.status.last_camera_sync = now_str

    result_message = ""
    detected_change = {}

    if req.action == "add_item":
        name = req.item_name or "Fresh Blueberries (1 Pint)"
        cat = req.category or "Groceries"
        qty = req.quantity or 1.0
        new_item = db.add_item({
            "name": name,
            "category": cat,
            "quantity": qty,
            "unit": "pack",
            "capacity": 1.0,
            "expiry_date": (date.today() + timedelta(days=7)).isoformat(),
            "shelf_location": "Middle Shelf",
            "temperature_target_min": 1.5,
            "temperature_target_max": 4.5,
            "price": 4.99,
            "auto_reorder_enabled": True,
            "requires_approval": False
        })
        result_message = f"AI Vision detected NEW item added: {name} (Category: {cat})"
        detected_change = {"type": "ADDED", "item": new_item}

    elif req.action == "consume_milk":
        # Simulate drinking remaining milk
        if "item_1" in db.items:
            milk = db.items["item_1"]
            milk.quantity = max(0.05, milk.quantity - 0.2)
            milk.stock_percent = int((milk.quantity / milk.capacity) * 100)
            db.evaluate_auto_replenishment()
            result_message = f"AI Vision detected level drop in {milk.name}. Stock now at {milk.stock_percent}%."
            detected_change = {"type": "CONSUMED", "item": milk}
        else:
            result_message = "Milk is already finished."

    elif req.action == "remove_meal":
        # Simulate user taking out leftover meal
        if "item_6" in db.items:
            removed = db.items.pop("item_6")
            result_message = f"AI Vision detected item REMOVED: {removed.name}"
            detected_change = {"type": "REMOVED", "item": removed}
        else:
            result_message = "Meal prep was already taken out."

    else:
        # Simple cycle without modification
        result_message = "Door opened and closed. No inventory delta detected."
        detected_change = {"type": "NO_CHANGE"}

    return {
        "status": "success",
        "timestamp": now_str,
        "door_cycles_today": db.status.door_open_count_today,
        "ai_analysis": result_message,
        "detected_change": detected_change,
        "active_inventory_count": len(db.items),
        "pending_orders": len(db.reorders)
    }

# --- REPLENISHMENT & PAYMENT GATEWAY MOCK ---

@app.get("/api/reorder", response_model=List[ReorderItem])
def get_reorders():
    return db.reorders

@app.post("/api/reorder/{order_id}/approve")
def approve_reorder(order_id: str):
    success = db.approve_order(order_id)
    if not success:
        raise HTTPException(status_code=400, detail="Order not found or already approved")
    return {"message": f"Order {order_id} approved and sent to fulfillment supplier."}

@app.post("/api/reorder/trigger")
def trigger_replenishment_check():
    db.evaluate_auto_replenishment()
    return {"message": "Auto-replenishment evaluation completed", "active_orders": len(db.reorders)}

# --- ANALYTICS & PREDICTION ---

@app.get("/api/analytics")
def get_analytics():
    items = db.get_all_items()
    categories = {}
    for item in items:
        categories[item.category] = categories.get(item.category, 0) + 1

    low_stock_items = [i for i in items if i.status == "Low Stock"]
    expiring_soon_items = [i for i in items if i.status in ["Expiring Soon", "Expired"]]
    optimal_items = [i for i in items if i.status == "Optimal"]

    # Predictive runout dates
    runout_forecasts = []
    for i in items:
        days_left = round(i.quantity / max(i.consumption_rate_per_day, 0.05), 1)
        runout_forecasts.append({
            "item_name": i.name,
            "category": i.category,
            "current_stock": f"{i.quantity} {i.unit}",
            "estimated_days_remaining": days_left,
            "predicted_stockout": (date.today() + timedelta(days=int(days_left))).isoformat()
        })

    return {
        "summary": {
            "total_items": len(items),
            "optimal_count": len(optimal_items),
            "low_stock_count": len(low_stock_items),
            "expiring_count": len(expiring_soon_items),
            "monthly_budget": db.settings.monthly_budget,
            "monthly_spent": db.settings.spent_this_month
        },
        "category_distribution": categories,
        "runout_forecasts": sorted(runout_forecasts, key=lambda x: x["estimated_days_remaining"])[:5]
    }

# --- SETTINGS & BUDGET CONFIGURATION ---

@app.get("/api/settings", response_model=SettingsConfig)
def get_settings():
    return db.settings

@app.put("/api/settings", response_model=SettingsConfig)
def update_settings(new_settings: SettingsConfig):
    db.settings = new_settings
    return db.settings
