# app/api/endpoints/detection.py
import os
import tempfile
from fastapi import APIRouter, File, UploadFile
from app.utils import detection_utils

router = APIRouter()

@router.post("/")
async def detect_number_plate(image: UploadFile = File(...)):
    # Save the uploaded image to a temporary file
    suffix = os.path.splitext(image.filename)[1] if image.filename else ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        contents = await image.read()
        temp_file.write(contents)
        temp_file_path = temp_file.name

    try:
        # Run detection using your YOLOv8 model
        detections = detection_utils.detect_number_plate(temp_file_path)
    except Exception as e:
        os.remove(temp_file_path)
        return {"status": "error", "message": str(e)}

    # Clean up the temporary file
    os.remove(temp_file_path)
    
    return {"status": "success", "detections": detections}
