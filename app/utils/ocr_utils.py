# app/utils/ocr_utils.py
import cv2
import easyocr
import os
import numpy as np

reader = easyocr.Reader(['en'], gpu=True)

def crop_image(image_path: str, bbox: list):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")
    xmin, ymin, xmax, ymax = map(int, bbox)
    cropped = image[ymin:ymax, xmin:xmax]
    return cropped

def ocr_plate(cropped_image, debug=False):
    """
    Applies thresholding and morphological operations before running OCR.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Slight blur to reduce noise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Morphological dilation
    kernel = np.ones((2, 2), np.uint8)
    morph = cv2.dilate(thresh, kernel, iterations=1)

    # Convert back to RGB for EasyOCR
    rgb_image = cv2.cvtColor(morph, cv2.COLOR_GRAY2RGB)

    if debug:
        os.makedirs("debug", exist_ok=True)
        cv2.imwrite("debug/cropped_original.jpg", cropped_image)
        cv2.imwrite("debug/gray.jpg", gray)
        cv2.imwrite("debug/thresh.jpg", thresh)
        cv2.imwrite("debug/morph.jpg", morph)
        cv2.imwrite("debug/final_rgb.jpg", rgb_image)
        print("Debug images saved in the 'debug' folder.")

    result = reader.readtext(rgb_image, detail=0, paragraph=True)
    print("EasyOCR raw result:", result)
    text = " ".join(result).strip()
    return text
