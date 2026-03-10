from sqlalchemy.orm import Session
from app.services import authServices
from app.helpers.response_helper import ResponseHelper
from app.helpers.constants import SUCCESS_MSGS, ERROR_MSGS

async def create_greet(data, db: Session):

    try:
        result = await authServices.create_greet(data, db)
        return ResponseHelper.success(SUCCESS_MSGS.GREETING_SAVED,
                                      result)
    except Exception as error:
        return ResponseHelper.error(str(error), ERROR_MSGS.INTERNAL_SERVER_ERROR)
