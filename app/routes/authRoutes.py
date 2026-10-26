from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth_schemas import ISignupStart, ISignupDetailsRequest, ISignupPhoto, ISignupComplete
from app.schemas.auth_schemas import ISigninStart, ISigninVerify
from app.database import get_db
from app.controllers import authControllers
from app.models.authmodels import VerifiedUser
from app.dependencies.auth import get_current_user

from app.schemas.auth_schemas import ISigninStart, ISigninVerify
router = APIRouter()


@router.get("/")
def get_auth():
    return {"message": "Auth routes"}


@router.post("/signup/start")
async def signupStart(data: ISignupStart, db: Session = Depends(get_db)):
    print(data)
    return await authControllers.signupStart(data, db)


@router.post("/signup/details")
async def signupDetails(data: ISignupDetailsRequest, db: Session = Depends(get_db)):
    return await authControllers.signupDetails(data, db)

# @router.post("/signup/photo")
# async def signupDetails(data: ISignupDetailsRequest, db: Session = Depends(get_db)):
#     return await authControllers.signupDe(data, db)

@router.post("/signup/photo")
async def signupPhoto(data: ISignupPhoto, db: Session = Depends(get_db)):
    return await authControllers.signupPhoto(data, db)

@router.post("/signup/complete")
async def signupComplete(data: ISignupComplete, db: Session = Depends(get_db)):
    return await authControllers.signupComplete(data, db)


@router.post("/signin/start")
async def signinStart(data: ISigninStart, db: Session = Depends(get_db)):
    return await authControllers.signinStart(data, db)

@router.post("/signin/verify")
async def signinVerify(data: ISigninVerify, db: Session = Depends(get_db)):
    return await authControllers.signinVerify(data, db)

@router.get("/v1/profile")
async def get_profile(current_user: VerifiedUser = Depends(get_current_user)):
    return await authControllers.getProfile(current_user)
