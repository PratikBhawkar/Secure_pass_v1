# app/api/endpoints/ocr.py
import os
import tempfile
from fastapi import APIRouter, File, UploadFile
from app.utils import detection_utils, ocr_utils, text_processing

router = APIRouter()

@router.post("/ocr")
async def detect_and_ocr(image: UploadFile = File(...)):
    suffix = os.path.splitext(image.filename)[1] if image.filename else ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        contents = await image.read()
        temp_file.write(contents)
        temp_file_path = temp_file.name

    detections = detection_utils.detect_number_plate(temp_file_path)
    ocr_results = []
    
    if detections:
        for detection in detections:
            bbox = detection.get("bbox")
            try:
                cropped = ocr_utils.crop_image(temp_file_path, bbox)
            except Exception as e:
                print(f"Error cropping image: {e}")
                continue
            
            # Use debug mode during development
            raw_text = ocr_utils.ocr_plate(cropped, debug=True)
            print(f"Raw OCR text for bbox {bbox}: '{raw_text}'")
            
            final_text = text_processing.process_plate_text(raw_text)
            print(f"Processed OCR text: '{final_text}'")
            
            original_conf = detection.get("confidence", 0)
            adjusted_conf = text_processing.apply_last_four_bonus(final_text, original_conf, bonus=0.1)
            
            ocr_results.append({
                "bbox": bbox,
                "confidence": original_conf,
                "adjusted_confidence": adjusted_conf,
                "class": detection.get("class"),
                "text": final_text
            })
    else:
        ocr_results = []
    
    os.remove(temp_file_path)
    return {"status": "success", "ocr_results": ocr_results}
