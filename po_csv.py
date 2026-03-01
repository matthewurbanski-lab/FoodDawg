import csv
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Iterable

from app.core.config import settings
from app.schemas.purchasing import POIn, POLineIn
from app.services.integrations.po_base import PurchaseOrderSource

class CSVPurchaseOrderSource(PurchaseOrderSource):
    async def fetch_pos(self, start: date | None = None, end: date | None = None) -> Iterable[POIn]:
        path = Path(settings.po_csv_path)
        if not path.exists():
            return []

        grouped: dict[str, dict] = defaultdict(lambda: {"vendor": "", "received_date": None, "lines": []})

        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                po = r["po_number"].strip()
                vendor = r["vendor"].strip()
                received = date.fromisoformat(r["received_date"])
                if start and received < start:
                    continue
                if end and received > end:
                    continue

                grouped[po]["vendor"] = vendor
                grouped[po]["received_date"] = received
                grouped[po]["lines"].append(
                    POLineIn(
                        sku=r["sku"].strip(),
                        description=r["description"].strip(),
                        qty=float(r["qty"]),
                        unit=r["unit"].strip(),
                        unit_price=float(r["unit_price"]),
                    )
                )

        return [
            POIn(po_number=po_number, vendor=v["vendor"], received_date=v["received_date"], lines=v["lines"])
            for po_number, v in grouped.items()
        ]
