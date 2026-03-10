from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.greet_schema import GreetRequest
from app.database import get_db
from app.controllers import authControllers

router = APIRouter()


@router.get("/")
def get_auth():
    return {"message": "Auth routes"}


@router.post("/greet")
async def greet(data: GreetRequest, db: Session = Depends(get_db)):
    return await authControllers.create_greet(data, db)

