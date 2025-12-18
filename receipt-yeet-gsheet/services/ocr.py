import os
import json
import base64
import requests


def ocr_image(image_path: str) -> str:
    api_key = os.getenv("GOOGLE_VISION_API_KEY")
    
    try:
        with open(image_path, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    payload = {
        "requests": [
            {
                "image": {"content": base64.b64encode(content).decode("utf-8")},
                "features": [{"type": "TEXT_DETECTION"}],
                "imageContext": {"languageHints": ["ja", "en"]},
            }
        ]
    }
    
    url = "https://vision.googleapis.com/v1/images:annotate"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    responses = data.get("responses", [])
    
    if not responses:
        return ""
    
    resp0 = responses[0]
    
    full_text = resp0.get("fullTextAnnotation", {}).get("text")
    if full_text:
        return full_text.strip()
    
    # fallback to textAnnotations
    annotations = resp0.get("textAnnotations", [])
    if annotations:
        return annotations[0].get("description", "").strip()
	


if __name__ == "__main__":
    from dotenv import load_dotenv
    
    load_dotenv()
    
    test_image = "/Users/mits-mac-001/Code/receipt-yeet-gsheet/test3.jpg"
    result = ocr_image(test_image)
    print(result if result else "No text detected")