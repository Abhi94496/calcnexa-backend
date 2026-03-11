from pydantic import BaseModel
from typing import Optional

class ISignupStart(BaseModel):
    phone : Optional[str] = None
    email : Optional[str] = None

class ISignupDetailsRequest(BaseModel):
    uuid: str
    phone: str
    email: str
    first_name: str
    last_name: str
    organization_name: str
    password: str

class ISignupPhoto(BaseModel):
    uuid: str
    profile_photo_url : Optional[str] = None

class ISignupComplete(BaseModel):
    uuid: str
