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
            message= SUCCESS_MSGS.SIGNUP_START_SUCCESSFUL, 
            data=result
        )

    except Exception as e:
        return ResponseHelper.error(
            message=str(e),
            error_type=ERROR_MSGS.SIGNUP_START_FAILED
        )
    

async def signupDetails(data, db: Session):
    result = await authServices.signupDetails(data, db)
    if result.get("status") == "error":
        return result
    
    return ResponseHelper.success(
        message= SUCCESS_MSGS.DETAILS_SAVED, 
        data=result
    )

async def signupPhoto(data, db):

    result = await authServices.signupPhoto(data, db)

    if result.get("status") == "error":
        return result

    return ResponseHelper.success(
        message=SUCCESS_MSGS.PHOTO_SAVED_SUCCESFUL,
        data=result
    )



async def signupComplete(data, db):

    result = await authServices.signupComplete(data, db)

    # if service returned error
    if result.get("status") == "error":
        return result

    return ResponseHelper.success(
        message= SUCCESS_MSGS.SIGNUP_SUCCESSFUL
    )

# SIGN IN
async def signinStart(data, db: Session):

    result = await authServices.signinStart(data, db)

    if result.get("status") == "error":
        return result

    return ResponseHelper.success(
        message=SUCCESS_MSGS.SIGNIN_START,
        data=result
    )

async def signinVerify(data, db: Session):

    result = await authServices.signinVerify(data, db)

    if result.get("status") == "error":
        return result

    return ResponseHelper.success(
        message=SUCCESS_MSGS.SIGNIN_SUCCESSFULL,
        data=result
    )