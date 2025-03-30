# test_integration.py
from app.utils.detection_utils import load_yolo_model, detect_number_plate
from app.utils.ocr_utils import crop_image, ocr_plate
from app.utils.text_processing import get_final_plate_text

def run_integration(image_path: str):
    model = load_yolo_model()
    detections = detect_number_plate(image_path, model=model, conf_threshold=0.25)
    for det in detections:
        bbox = det["bbox"]
        cropped = crop_image(image_path, bbox)
        raw_ocr = ocr_plate(cropped, debug=True)
        
        # Enforce the strict format
        final_plate = get_final_plate_text(raw_ocr)
        
        print(f"Raw OCR: {raw_ocr}")
        print(f"Final Plate (Strict Format): '{final_plate}'" if final_plate else "No valid plate found")

if __name__ == "__main__":
    test_image = r"C:\Users\PRATIK\SECURE_PASS_BACKEND\data\our database\WhatsApp Image 2025-03-19 at 11.38.07_bb7e11e6.jpg"
    run_integration(test_image)
