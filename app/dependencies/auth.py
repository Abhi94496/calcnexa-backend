# FastAPI
from fastapi import Depends, HTTPException
# Security (for Bearer token)
from fastapi.security import OAuth2PasswordBearer
# JWT
from jose import JWTError, ExpiredSignatureError, jwt
# Database
from sqlalchemy.orm import Session
# Your project imports
from app.database import get_db
from app.models.authmodels import VerifiedUser
from app.core.config import SECRET_KEY, ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(VerifiedUser).filter(
        VerifiedUser.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
