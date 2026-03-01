from datetime import date
from typing import Iterable

import httpx

from app.core.config import settings
from app.schemas.purchasing import POIn
from app.services.integrations.po_base import PurchaseOrderSource

class RESTPurchaseOrderSource(PurchaseOrderSource):
    """Skeleton REST adapter. Implement mapping to your PO system."""

    async def fetch_pos(self, start: date | None = None, end: date | None = None) -> Iterable[POIn]:
        headers = {}
        if settings.po_rest_token:
            headers["Authorization"] = f"Bearer {settings.po_rest_token}"

        params = {}
        if start:
            params["start"] = start.isoformat()
        if end:
            params["end"] = end.isoformat()

        async with httpx.AsyncClient(base_url=settings.po_rest_base_url, headers=headers, timeout=30) as client:
            r = await client.get("/purchase-orders", params=params)
            r.raise_for_status()
            data = r.json()

        return [POIn.model_validate(x) for x in data]
