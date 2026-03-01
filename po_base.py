from abc import ABC, abstractmethod
from datetime import date
from typing import Iterable

from app.schemas.purchasing import POIn

class PurchaseOrderSource(ABC):
    @abstractmethod
    async def fetch_pos(self, start: date | None = None, end: date | None = None) -> Iterable[POIn]:
        """Return purchase orders (with lines)."""
        raise NotImplementedError
