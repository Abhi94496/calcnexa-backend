from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers import procurementControllers
from app.schemas.procurement_schemas import (
    ICreatePurchaseRequest,
    IUpdatePurchaseRequestStatus,
)

router = APIRouter()


@router.get("/")
def procurement_health():
    return {"message": "Procurement routes"}


@router.post("/purchase-requests")
async def create_purchase_request(data: ICreatePurchaseRequest, db: Session = Depends(get_db)):
    return await procurementControllers.createPurchaseRequest(data, db)


@router.get("/purchase-requests")
async def list_purchase_requests(db: Session = Depends(get_db)):
    return await procurementControllers.listPurchaseRequests(db)


@router.get("/purchase-requests/{request_id}")
async def get_purchase_request(request_id: str, db: Session = Depends(get_db)):
    return await procurementControllers.getPurchaseRequest(request_id, db)


@router.patch("/purchase-requests/{request_id}/status")
async def update_purchase_request_status(
    request_id: str,
    data: IUpdatePurchaseRequestStatus,
    db: Session = Depends(get_db),
):
    return await procurementControllers.updatePurchaseRequestStatus(request_id, data.status, db)
