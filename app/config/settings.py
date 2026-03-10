from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name : str
    authorization_enabled : bool

    class Config:
        env_file = ".env"

settings = Settings()