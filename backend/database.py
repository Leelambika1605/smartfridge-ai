import uuid
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
from models import InventoryItem, FridgeStatus, ReorderItem, SettingsConfig

class FridgeDatabase:
    def __init__(self):
        today = date.today()
        self.status = FridgeStatus(
            temperature=3.6,
            humidity=58.2,
            door_state="Closed",
            door_open_count_today=8,
            cooling_health="Optimal",
            last_door_cycle=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            last_camera_sync=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self.settings = SettingsConfig()

        # Initial seed items representing diverse real-world refrigerator contents
        self.items: Dict[str, InventoryItem] = {
            "item_1": InventoryItem(
                id="item_1",
                name="Organic Whole Milk",
                category="Groceries",
                quantity=0.25,
                unit="liters",
                capacity=1.0,
                stock_percent=25,
                expiry_date=(today + timedelta(days=2)).isoformat(),
                shelf_location="Door Bin 1",
                temperature_target_min=1.0,
                temperature_target_max=4.0,
                price=4.20,
                auto_reorder_enabled=True,
                requires_approval=False,
                consumption_rate_per_day=0.35
            ),
            "item_2": InventoryItem(
                id="item_2",
                name="Pasture-Raised Eggs (Dozen)",
                category="Groceries",
                quantity=3,
                unit="pcs",
                capacity=12,
                stock_percent=25,
                expiry_date=(today + timedelta(days=14)).isoformat(),
                shelf_location="Top Shelf",
                temperature_target_min=2.0,
                temperature_target_max=7.0,
                price=5.80,
                auto_reorder_enabled=True,
                requires_approval=False,
                consumption_rate_per_day=1.5
            ),
            "item_3": InventoryItem(
                id="item_3",
                name="Insulin Glargine (Lantus) Pen",
                category="Medicines",
                quantity=1,
                unit="cartridge",
                capacity=1,
                stock_percent=30,
                expiry_date=(today + timedelta(days=45)).isoformat(),
                shelf_location="Medicine Lockbox Shelf",
                temperature_target_min=2.0,
                temperature_target_max=8.0,
                price=85.00,
                auto_reorder_enabled=True,
                requires_approval=True, # Safety check: medicines require user sign-off
                consumption_rate_per_day=0.03
            ),
            "item_4": InventoryItem(
                id="item_4",
                name="Cold-Pressed Orange Juice",
                category="Beverages",
                quantity=0.8,
                unit="liters",
                capacity=1.0,
                stock_percent=80,
                expiry_date=(today + timedelta(days=6)).isoformat(),
                shelf_location="Middle Shelf",
                temperature_target_min=2.0,
                temperature_target_max=6.0,
                price=6.50,
                auto_reorder_enabled=True,
                requires_approval=False,
                consumption_rate_per_day=0.2
            ),
            "item_5": InventoryItem(
                id="item_5",
                name="Active Retinol & Hyaluronic Serum",
                category="Skincare",
                quantity=25,
                unit="ml",
                capacity=30,
                stock_percent=83,
                expiry_date=(today + timedelta(days=180)).isoformat(),
                shelf_location="Skincare Door Pocket",
                temperature_target_min=4.0,
                temperature_target_max=10.0,
                price=34.00,
                auto_reorder_enabled=False,
                requires_approval=True,
                consumption_rate_per_day=0.5
            ),
            "item_6": InventoryItem(
                id="item_6",
                name="Meal Prep: Herb Grilled Chicken",
                category="Prepared Food",
                quantity=1,
                unit="container",
                capacity=1,
                stock_percent=100,
                expiry_date=(today + timedelta(days=1)).isoformat(),
                shelf_location="Crisper Zone",
                temperature_target_min=1.0,
                temperature_target_max=4.0,
                price=0.0,
                auto_reorder_enabled=False,
                requires_approval=False,
                consumption_rate_per_day=0.5
            ),
            "item_7": InventoryItem(
                id="item_7",
                name="Sparkling Lime Mineral Water (6pk)",
                category="Beverages",
                quantity=5,
                unit="cans",
                capacity=6,
                stock_percent=83,
                expiry_date=(today + timedelta(days=90)).isoformat(),
                shelf_location="Bottom Shelf",
                temperature_target_min=2.0,
                temperature_target_max=8.0,
                price=7.99,
                auto_reorder_enabled=True,
                requires_approval=False,
                consumption_rate_per_day=0.8
            ),
            "item_8": InventoryItem(
                id="item_8",
                name="Greek Yogurt Plain 0% (32oz)",
                category="Groceries",
                quantity=0.15,
                unit="kg",
                capacity=0.9,
                stock_percent=16,
                expiry_date=(today + timedelta(days=4)).isoformat(),
                shelf_location="Middle Shelf",
                temperature_target_min=2.0,
                temperature_target_max=5.0,
                price=5.29,
                auto_reorder_enabled=True,
                requires_approval=False,
                consumption_rate_per_day=0.15
            )
        }

        self.reorders: List[ReorderItem] = [
            ReorderItem(
                id="ord_101",
                item_id="item_1",
                item_name="Organic Whole Milk",
                category="Groceries",
                quantity_to_order=1.0,
                unit="liters",
                estimated_cost=4.20,
                status="In Transit",
                created_at=(datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
                supplier="Instacart Fresh Express",
                requires_approval=False
            ),
            ReorderItem(
                id="ord_102",
                item_id="item_3",
                item_name="Insulin Glargine (Lantus) Pen",
                category="Medicines",
                quantity_to_order=1.0,
                unit="cartridge",
                estimated_cost=85.00,
                status="Pending Approval",
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
                supplier="CVS Health / PillPack",
                requires_approval=True
            )
        ]

    def _enrich_item(self, item: InventoryItem) -> InventoryItem:
        # Calculate days until expiry
        today = date.today()
        try:
            exp_date = datetime.strptime(item.expiry_date, "%Y-%m-%d").date()
            diff = (exp_date - today).days
            item.days_until_expiry = diff
        except Exception:
            item.days_until_expiry = 999

        # Calculate Status
        if item.days_until_expiry <= 0:
            item.status = "Expired"
        elif item.days_until_expiry <= 2:
            item.status = "Expiring Soon"
        elif item.stock_percent <= 25:
            item.status = "Low Stock"
        elif self.status.temperature > item.temperature_target_max or self.status.temperature < item.temperature_target_min:
            item.status = "Temp Alert"
        else:
            item.status = "Optimal"

        return item

    def get_all_items(self) -> List[InventoryItem]:
        return [self._enrich_item(item) for item in self.items.values()]

    def get_item(self, item_id: str) -> InventoryItem:
        if item_id in self.items:
            return self._enrich_item(self.items[item_id])
        return None

    def add_item(self, item_data: dict) -> InventoryItem:
        new_id = f"item_{uuid.uuid4().hex[:6]}"
        stock_pct = int(min(100, max(0, (item_data['quantity'] / max(item_data['capacity'], 0.001)) * 100)))
        item = InventoryItem(
            id=new_id,
            stock_percent=stock_pct,
            **item_data
        )
        self.items[new_id] = item
        self.status.last_camera_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.evaluate_auto_replenishment()
        return self._enrich_item(item)

    def delete_item(self, item_id: str) -> bool:
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False

    def update_item_quantity(self, item_id: str, new_quantity: float) -> InventoryItem:
        if item_id in self.items:
            item = self.items[item_id]
            item.quantity = max(0.0, new_quantity)
            item.stock_percent = int(min(100, max(0, (item.quantity / max(item.capacity, 0.001)) * 100)))
            self.evaluate_auto_replenishment()
            return self._enrich_item(item)
        return None

    def evaluate_auto_replenishment(self):
        """Scans inventory for items running low or about to expire, triggering auto-orders."""
        for item in self.get_all_items():
            if not item.auto_reorder_enabled:
                continue

            # Don't place duplicates if active order exists
            has_active_order = any(
                r.item_id == item.id and r.status in ["Pending Approval", "Approved & Placed", "In Transit"]
                for r in self.reorders
            )
            if has_active_order:
                continue

            needs_reorder = (item.stock_percent <= 25) or (item.days_until_expiry is not None and item.days_until_expiry <= 2)

            if needs_reorder:
                # Check security approval condition
                needs_manual_approval = (
                    item.category == "Medicines"
                    or item.price >= self.settings.approval_threshold_price
                    or item.requires_approval
                    or (self.settings.spent_this_month + item.price > self.settings.monthly_budget)
                )

                initial_status = "Pending Approval" if needs_manual_approval else "Approved & Placed"
                
                # If automatically placed without manual approval, record payment deduction
                if initial_status == "Approved & Placed" and self.settings.auto_pay_enabled:
                    self.settings.spent_this_month = round(self.settings.spent_this_month + item.price, 2)

                new_order = ReorderItem(
                    id=f"ord_{uuid.uuid4().hex[:6]}",
                    item_id=item.id,
                    item_name=item.name,
                    category=item.category,
                    quantity_to_order=item.capacity,
                    unit=item.unit,
                    estimated_cost=item.price,
                    status=initial_status,
                    created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
                    supplier="Instacart QuickFresh" if item.category != "Medicines" else "CVS Health Online",
                    requires_approval=needs_manual_approval
                )
                self.reorders.insert(0, new_order)

    def approve_order(self, order_id: str) -> bool:
        for ord in self.reorders:
            if ord.id == order_id and ord.status == "Pending Approval":
                ord.status = "Approved & Placed"
                self.settings.spent_this_month = round(self.settings.spent_this_month + ord.estimated_cost, 2)
                return True
        return False

# Global singleton database instance
db = FridgeDatabase()
