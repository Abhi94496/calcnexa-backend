from pydantic import BaseModel
from typing import Optional


class ICreatePurchaseRequest(BaseModel):
    item_name: str
    description: Optional[str] = None
    quantity: int
    unit_price: Optional[int] = None
    currency: str = "INR"
    department: Optional[str] = None


class IUpdatePurchaseRequestStatus(BaseModel):
    status: str
