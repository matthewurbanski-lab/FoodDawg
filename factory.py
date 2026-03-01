from app.core.config import settings
from app.services.integrations.po_base import PurchaseOrderSource
from app.services.integrations.po_csv import CSVPurchaseOrderSource
from app.services.integrations.po_rest import RESTPurchaseOrderSource

def get_po_source() -> PurchaseOrderSource:
    source = (settings.po_source or "csv").lower()
    if source == "rest":
        return RESTPurchaseOrderSource()
    return CSVPurchaseOrderSource()
