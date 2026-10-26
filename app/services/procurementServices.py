from sqlalchemy.orm import Session
from app.helpers.response_helper import ResponseHelper
from app.helpers.constants import ERROR_TYPES, ERROR_MSGS
from app.models.procurement_models import PurchaseRequest


async def createPurchaseRequest(data, db: Session):
    purchase_request = PurchaseRequest(
        item_name=data.item_name,
        description=data.description,
        quantity=data.quantity,
        unit_price=data.unit_price,
        currency=data.currency,
        department=data.department,
        status="SUBMITTED"
    )

    db.add(purchase_request)
    db.commit()
    db.refresh(purchase_request)

    return {
        "id": str(purchase_request.id),
        "item_name": purchase_request.item_name,
        "status": purchase_request.status,
        "quantity": purchase_request.quantity,
        "currency": purchase_request.currency,
    }


async def listPurchaseRequests(db: Session):
    rows = db.query(PurchaseRequest).order_by(PurchaseRequest.created_at.desc()).all()
    data = []
    for row in rows:
        data.append(
            {
                "id": str(row.id),
                "item_name": row.item_name,
                "status": row.status,
                "quantity": row.quantity,
                "unit_price": row.unit_price,
                "currency": row.currency,
                "department": row.department,
            }
        )

    return data


async def getPurchaseRequest(request_id: str, db: Session):
    row = db.query(PurchaseRequest).filter(PurchaseRequest.id == request_id).first()

    if not row:
        return ResponseHelper.error(
            message=ERROR_MSGS.PROCUREMENT_REQUEST_NOT_FOUND,
            error_type=ERROR_TYPES.DATA_NOT_FOUND,
            status_code=404,
        )

    return {
        "id": str(row.id),
        "item_name": row.item_name,
        "description": row.description,
        "quantity": row.quantity,
        "unit_price": row.unit_price,
        "currency": row.currency,
        "department": row.department,
        "status": row.status,
    }


async def updatePurchaseRequestStatus(request_id: str, status: str, db: Session):
    row = db.query(PurchaseRequest).filter(PurchaseRequest.id == request_id).first()

    if not row:
        return ResponseHelper.error(
            message=ERROR_MSGS.PROCUREMENT_REQUEST_NOT_FOUND,
            error_type=ERROR_TYPES.DATA_NOT_FOUND,
            status_code=404,
        )

    row.status = status.upper()
    db.commit()
    db.refresh(row)

    return {
        "id": str(row.id),
        "status": row.status,
    }
