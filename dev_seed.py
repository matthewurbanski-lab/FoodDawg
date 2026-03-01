"""Optional: seed some sample inventory movements."""
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.inventory import Item, InventoryLedger

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    if not db.query(Item).filter_by(sku="SKU-TOM").first():
        item = Item(sku="SKU-TOM", description="Canned Tomatoes", unit="case")
        db.add(item)
        db.flush()
        db.add(InventoryLedger(item_id=item.id, qty=5, unit_cost=22.5, reference="seed"))
        db.commit()
finally:
    db.close()

print("Seeded.")
