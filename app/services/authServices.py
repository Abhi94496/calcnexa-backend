import uuid
from sqlalchemy.orm import Session
from app.models.authmodels import SignupSession, VerifiedUser
from app.helpers.response_helper import ResponseHelper
from app.helpers.constants import ERROR_TYPES, ERROR_MSGS

async def signupStart(phone: str, email: str, db: Session):
    # validation
    if not phone and not email:
        return ResponseHelper.error(
            message= ERROR_MSGS.PHONE_MAIL_REQUIRED,
            error_type= ERROR_TYPES.BAD_REQUEST
        )

    # Check verified users
    verified_user = db.query(VerifiedUser).filter(
        (VerifiedUser.phone == phone) |
        (VerifiedUser.email == email)
    ).first()

    if verified_user:
        return ResponseHelper.error(
            message= ERROR_MSGS.USER_ALREADY_EXIST,
            error_type= ERROR_TYPES.ALREADY_EXISTS
        )

    # Check signup session (resume signup)
    signup_session = db.query(SignupSession).filter(
        (SignupSession.phone == phone) |
        (SignupSession.email == email)
    ).first()

    if signup_session:
        return {
            "uuid": str(signup_session.id),
            "stage": signup_session.stage
        }

    # Create new signup session
    new_session = SignupSession(
        id=uuid.uuid4(),
        phone=phone,
        email=email,
        stage=0
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "uuid": str(new_session.id),
        "stage": new_session.stage
    }