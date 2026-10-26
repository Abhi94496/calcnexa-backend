from sqlalchemy.orm import Session
from app.services import procurementServices
from app.helpers.response_helper import ResponseHelper
from app.helpers.constants import SUCCESS_MSGS


async def createPurchaseRequest(data, db: Session):
    result = await procurementServices.createPurchaseRequest(data, db)
    if result.get("status") == "error":
        return result

    return ResponseHelper.success(
        message=SUCCESS_MSGS.PROCUREMENT_REQUEST_CREATED,
        data=result,
    )


async def listPurchaseRequests(db: Session):
    result = await procurementServices.listPurchaseRequests(db)
    return ResponseHelper.success(
        message=SUCCESS_MSGS.PROCUREMENT_REQUESTS_FETCHED,
        data=result,
    )


async def getPurchaseRequest(request_id: str, db: Session):
    result = await procurementServices.getPurchaseRequest(request_id, db)
    if result.get("status") == "error":
        return result

    return ResponseHelper.success(
        message=SUCCESS_MSGS.PROCUREMENT_REQUEST_FETCHED,
        data=result,
    )


async def updatePurchaseRequestStatus(request_id: str, status: str, db: Session):
    result = await procurementServices.updatePurchaseRequestStatus(request_id, status, db)
    if result.get("status") == "error":
        return result

    return ResponseHelper.success(
        message=SUCCESS_MSGS.PROCUREMENT_REQUEST_UPDATED,
        data=result,
    )
