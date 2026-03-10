from fastapi import FastAPI
from app.routes.authRoutes import router as authRoutes
from app.database import base, engine
import app.models.greet_model  # noqa: F401
from dotenv import load_dotenv
import os
load_dotenv()
serverPort = os.getenv("SERVER_PORT")

app = FastAPI()

app.include_router(authRoutes, prefix = "/auth")
base.metadata.create_all(bind=engine)


@app.on_event("startup")
def create_tables():
    # Importing model above ensures SQLAlchemy metadata includes the table.
    base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return { "message" : "Calcnexa running" }




print(f"server running in {serverPort}")
