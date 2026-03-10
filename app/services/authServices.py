from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.greet_model import Greet


async def create_greet(payload, db: Session):
    greet = Greet(
        phone_number=payload.phone_number,
        greeting=payload.greeting,
    )

    try:
        db.add(greet)
        db.commit()
        db.refresh(greet)
        return {
            "id": greet.id,
            "phone_number": greet.phone_number,
            "greeting": greet.greeting,
        }
    except SQLAlchemyError:
        db.rollback()
        raise

    