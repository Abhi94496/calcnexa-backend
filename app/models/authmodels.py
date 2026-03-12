import uuid
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.database import base


class SignupSession(base):
    __tablename__ = "signup_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String(255), unique=True, nullable=True)
    phone = Column(String(20), unique=True, nullable=True)

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    organization_name = Column(String(255), nullable=True)
    password = Column(String, nullable=True)

    profile_photo_url = Column(String, nullable=True)
    photo_skipped = Column(Boolean, default=False)
    role = Column(Integer, nullable=True)
    stage = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )



class VerifiedUser(base):
    __tablename__ = "verified_users"

    id = Column(UUID(as_uuid=True), primary_key=True)

    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    org_id = Column(UUID(as_uuid=True), nullable=False)
    # role = Column(Integer, nullable=False)
    profile_photo_url = Column(String, nullable=True)
    photo_skipped = Column(Boolean, default=False)
    password = Column(String, nullable=True)

    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class SigninTransaction(base):
    __tablename__ = "signin_transactions"

    transcid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)

    userid = Column(UUID(as_uuid=True), nullable=False)

    flow = Column(String(50), default="signin")

    created_at = Column(DateTime(timezone=True), server_default=func.now())