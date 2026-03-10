from sqlalchemy import Column, Integer, String
from app.database import base


class user(base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True, index = True)
    greeting = Column(String, nullable=False)
    name = Column(String, nullable= False)
    phone_number = Column(Integer, nullable= True)