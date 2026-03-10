from pydantic import BaseModel


class GreetRequest(BaseModel):
    phone_number : str
    greeting : str