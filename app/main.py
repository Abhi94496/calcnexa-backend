from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.authRoutes import router as authRoutes
from app.routes.procurementRoutes import router as procurementRoutes
from app.database import base, engine
from dotenv import load_dotenv
import os

load_dotenv()
serverPort = os.getenv("SERVER_PORT")

app = FastAPI()

# --- NEW: CORS MIDDLEWARE ---
# This explicitly tells FastAPI to accept cross-origin POST and OPTIONS requests from your VS Code browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)
# ----------------------------

app.include_router(authRoutes, prefix = "/auth")
app.include_router(procurementRoutes, prefix="/procurement")
base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return { "message" : "Calcnexa running" }

print(f"server running in {serverPort}")
