from sqlalchemy.orm import Session
from app.services import authServices
from app.helpers.response_helper import ResponseHelper
from app.helpers.constants import SUCCESS_MSGS, ERROR_MSGS

async def signupStart(data, db: Session):
    try:

        phone = data.phone
        email = data.email

        result = await authServices.signupStart(phone, email, db)

        return ResponseHelper.success(
            message="Signup started successfully",
            data=result
        )

    except Exception as e:
        return ResponseHelper.error(
            message=str(e),
            error_type="SIGNUP_START_FAILED"
        )