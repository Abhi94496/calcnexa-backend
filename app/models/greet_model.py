from sqlalchemy import Column, Integer, String
from app.database import base

class Greet(base):
    __tablename__ = "greet"

    id = Column(Integer, primary_key = True, index = True)
    phone_number = Column(String(15), nullable= False)
    greeting = Column(String, nullable=False)
