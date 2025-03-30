# app/api/endpoints/logs.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def log_access(plate: str, access_granted: bool):
    # Placeholder for logging access attempt to the database
    # You can later use SQLAlchemy to record this in a logs table
    return {"status": "logged", "plate": plate, "access_granted": access_granted}
