from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.inventory import Item, InventoryLedger

def get_on_hand(db: Session):
    stmt = (
        select(
            Item.sku,
            Item.description,
            Item.unit,
            func.coalesce(func.sum(InventoryLedger.qty), 0.0).label("on_hand"),
            func.sum(InventoryLedger.qty * InventoryLedger.unit_cost).label("value"),
        )
        .join(InventoryLedger, InventoryLedger.item_id == Item.id, isouter=True)
        .group_by(Item.id)
        .order_by(Item.sku)
    )
    rows = db.execute(stmt).all()
    result = []
    for sku, desc, unit, on_hand, value in rows:
        avg_cost = None
        if on_hand and value is not None:
            try:
                avg_cost = float(value) / float(on_hand)
            except ZeroDivisionError:
                avg_cost = None
        result.append({"sku": sku, "description": desc, "unit": unit, "on_hand": float(on_hand), "avg_cost": avg_cost})
    return result
