import base64
import requests
import os
from io import BytesIO
from PIL import Image

API_KEY = "AQ.Ab8RN6KKw2PW-ib9Xqf4jYxtWm9-YMBn5yrs6CdMnUW1KjDhRQ" # Yahan apni API Key daal dena bhai
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

def compress_image_to_base64(image_path, max_size=(800, 800), quality=70):
    """Image ko compress karke Base64 me convert karta hai taaki app hang na ho."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=quality)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Compression error: {e}")
        return None

def get_gemini_response(prompt, image_paths, system_instruction):
    """Gemini API ko request bhejta hai aur proper JSON parse karta hai."""
    parts = [{"text": f"{system_instruction}\nUser Query: {prompt}"}]
    
    for path in image_paths:
        if os.path.exists(path):
            b64_data = compress_image_to_base64(path)
            if b64_data:
                parts.append({
                    "inlineData": {
                        "mimeType": "image/jpeg",
                        "data": b64_data
                    }
                })

    payload = {"contents": [{"parts": parts}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        res = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            # Sahi Play Store level JSON parsing
            return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"❌ API Error: {res.status_code} - {res.text}"
    except Exception as e:
        return f"📶 Network Issue: {str(e)}"
      
