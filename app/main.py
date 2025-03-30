# app/main.py
from fastapi import FastAPI
import uvicorn

# Import the database engine and Base from your models
from app.core.database import engine
from app.core.models import Base

# Create all tables defined in models
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SECURE PASS BACKEND")

# Import and include your routers
from app.api import endpoints

app.include_router(endpoints.detection.router, prefix="/detection", tags=["Detection"])
app.include_router(endpoints.ocr.router, prefix="/ocr", tags=["OCR"])
app.include_router(endpoints.verification.router, prefix="/verification", tags=["Verification"])
app.include_router(endpoints.logs.router, prefix="/logs", tags=["Logs"])

@app.get("/")
async def root():
    return {"message": "Welcome to SECURE PASS BACKEND"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
