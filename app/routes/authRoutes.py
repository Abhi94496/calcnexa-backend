from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth_schemas import ISignupStart, ISignupDetailsRequest
from app.database import get_db
from app.controllers import authControllers

router = APIRouter()


@router.get("/")
def get_auth():
    return {"message": "Auth routes"}


# @router.post("/greet")
# async def greet(data: GreetRequest, db: Session = Depends(get_db)):
#     return await authControllers.create_greet(data, db)

# @router.post("/sigup/start")
# async def signupStart(data : ISignupStart, db : Session =  Depends(get_db)):
#     print(data)
#     return await authControllers.signupStart(data, db)

@router.post("/signup/start")
async def signupStart(data: ISignupStart, db: Session = Depends(get_db)):
    print(data)
    # return {"received": data}
    return await authControllers.signupStart(data, db)