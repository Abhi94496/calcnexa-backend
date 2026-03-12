import uuid
from sqlalchemy.orm import Session
from app.models.authmodels import SignupSession, VerifiedUser,SigninTransaction
from app.helpers.response_helper import ResponseHelper
from app.helpers.constants import ERROR_TYPES, ERROR_MSGS,FLOWS
from app.middleware.security import hash_password
from app.middleware.security import verify_password
from app.models.authmodels import VerifiedUser, SigninTransaction
from app.models.organization_module import Organization, OrgEmployee
from app.models.roles_modules import Role
from app.models.authmodels import VerifiedUser, SignupSession

# -----------------------------------------------------------------------------------------
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

# --------------------------------------------------------------------------------------------------

async def signupDetails(data, db):

    # Check signup session exists
    session = db.query(SignupSession).filter(
        SignupSession.id == data.uuid).first()

    if not session:
        return ResponseHelper.error(
            message=ERROR_MSGS.SOMETHING_WENT_WRONG
        )

    # Check user already exists in verified users
    existing_user = db.query(VerifiedUser).filter(
        (VerifiedUser.phone == data.phone) |
        (VerifiedUser.email == data.email)).first()

    if existing_user:
        return ResponseHelper.error(
            message=ERROR_MSGS.USER_ALREADY_EXIST
        )
    hashed_password = hash_password(data.password)
    # Update signup session
    session.phone = data.phone
    session.email = data.email
    session.first_name = data.first_name
    session.last_name = data.last_name
    session.organization_name = data.organization_name
    session.password = hashed_password
    session.stage = 1

    db.commit()
    db.refresh(session)

    return {
        "uuid": str(session.id),
        "stage": session.stage
    }

# --------------------------------------------------------------------------------------------------

async def signupPhoto(data, db):

    session = db.query(SignupSession).filter(
        SignupSession.id == data.uuid
    ).first()

    if not session:
        return ResponseHelper.error(
            message=ERROR_MSGS.SOMETHING_WENT_WRONG
        )

    # if photo exists
    if data.profile_photo_url:
        session.profile_photo_url = data.profile_photo_url
        session.photo_skipped = False
    else:
        session.photo_skipped = True

    session.stage = 2

    db.commit()
    db.refresh(session)

    return {
        "uuid": str(session.id),
        "stage": session.stage,
        # "photo_skipped": session.photo_skipped
    }


# --------------------------------------------------------------------------------------------------

async def signupComplete(data, db):
    try:

        verified_user = db.query(VerifiedUser).filter(
            VerifiedUser.id == data.uuid
        ).first()

        if verified_user:
            return {
                "user_id": str(verified_user.id)
            }

        session = db.query(SignupSession).filter(
            SignupSession.id == data.uuid
        ).first()

        if not session:
            return ResponseHelper.error(
                message=ERROR_MSGS.SOMETHING_WENT_WRONG
            )

        if session.stage < 2:
            return ResponseHelper.error(
                message=ERROR_MSGS.INVALID_USER
            )

        existing_user = db.query(VerifiedUser).filter(
            (VerifiedUser.phone == session.phone) |
            (VerifiedUser.email == session.email)
        ).first()

        if existing_user:
            return {
                "user_id": str(existing_user.id)
            }
        domain = session.email.split("@")[1]
        org_name = domain.split(".")[0]


        org = db.query(Organization).filter(
            Organization.domain == domain
        ).first()

        if org:
            return ResponseHelper.error(
                message=ERROR_MSGS.ORGANIZATION_EXIST
            )

        org = Organization(
            name=org_name,
            domain=domain,
            plan_id=1
        )

        db.add(org)
        db.flush()

        new_user = VerifiedUser(
            id=session.id,
            phone=session.phone,
            email=session.email,
            first_name=session.first_name,
            last_name=session.last_name,
            profile_photo_url=session.profile_photo_url,
            photo_skipped=session.photo_skipped,
            password=session.password,
            org_id=org.id
        )

        db.add(new_user)
        db.flush()

        employee = OrgEmployee(
             organization_id=org.id,
            user_id=new_user.id,
            email=new_user.email,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            role_id=1
            )

        db.add(employee)

        db.commit()

        return {
            "user_id": str(new_user.id),
            "organization_id": str(org.id),
            "role_id": 1
        }

    except Exception as e:
        db.rollback()
        return ResponseHelper.error(
            message=ERROR_MSGS.SIGNUP_FAILED
        )
    

#-------------------------------SIGN IN----------------------------------------------------------

async def signinStart(data, db):

    identifier = data.identifier

    # detect email or phone
    if "@" in identifier:
        email = identifier
        phone = None
    else:
        phone = identifier
        email = None


    # check if user exists
    user = db.query(VerifiedUser).filter(
        (VerifiedUser.email == email) |
        (VerifiedUser.phone == phone)
    ).first()

    if not user:
        return ResponseHelper.error(
            message=ERROR_MSGS.INVALID_USER
        )


    # create transaction
    transaction = SigninTransaction(
        transcid=uuid.uuid4(),
        email=email,
        phone=phone,
        userid=user.id,
        flow=FLOWS.SIGNIN
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)


    return {
        "transaction_id": str(transaction.transcid)
    }

# ----------------------------------------------------------------------------------------
async def signinVerify(data, db):

    transaction_id = data.transaction_id
    password = data.password

    transaction = db.query(SigninTransaction).filter(
        SigninTransaction.transcid == transaction_id
    ).first()

    if not transaction:
        return ResponseHelper.error(ERROR_MSGS.INVALID_TRANSACTION)

    user = db.query(VerifiedUser).filter(
        VerifiedUser.id == transaction.userid
    ).first()

    if not user:
        return ResponseHelper.error(ERROR_MSGS.INVALID_USER)

    if not verify_password(password, user.password):
        return ResponseHelper.error(ERROR_MSGS.WRONG_PASSWORD)

    return {
        "user_id": str(user.id)
    }