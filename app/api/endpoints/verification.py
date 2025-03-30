# app/api/endpoints/verification.py
from fastapi import APIRouter, HTTPException
from app.core.database import SessionLocal
from app.core.models import AuthorizedVehicle, AccessLog
import datetime

router = APIRouter()

@router.post("/verify")
def verify_plate(plate: str, confidence: float):
    """
    Verifies the provided plate number against the authorized vehicles.
    Logs the access attempt with the confidence and verification result.
    """
    db = SessionLocal()
    try:
        # Query the database to check if the plate is authorized
        vehicle = db.query(AuthorizedVehicle).filter(
            AuthorizedVehicle.plate_number == plate
        ).first()
        
        # Determine if the plate is authorized
        is_authorized = vehicle is not None
        
        # Create a log entry
        log_entry = AccessLog(
            plate_number=plate,
            confidence=int(confidence * 100),  # Convert to integer percentage if desired
            verified=is_authorized
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
    
    return {
        "plate": plate,
        "authorized": is_authorized,
        "log_id": log_entry.id,
        "timestamp": log_entry.timestamp.isoformat()
    }
