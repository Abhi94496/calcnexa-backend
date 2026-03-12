
import uuid
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.database import base
import datetime

class Organization(base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    name = Column(String(255), unique=True, nullable=False)
    domain = Column(String(255), unique=True, nullable=False)

    plan_id = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OrgEmployee(base):
    __tablename__ = "org_employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    organization_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)

    email = Column(String(255), nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    role_id = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Plan(base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    user_limit = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())