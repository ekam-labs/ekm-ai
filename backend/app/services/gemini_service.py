import json
import requests
from app.config import GOOGLE_API, GEMINI3_FLASH, GEMINI25_FLASH, GEMMA3, REQUEST_TIMEOUT


def call_gemini(model_pick, messages, identity_prompt):

    if model_pick == "gemini-3-flash-preview":
        selected_model = GEMINI3_FLASH
    elif model_pick == "gemini_2.5-flash":
        selected_model = GEMINI25_FLASH
    elif model_pick == "gemma_v3":
        selected_model = GEMMA3
    else:
        return "Invalid Gemini model"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{selected_model}:generateContent?key={GOOGLE_API}"

    parts = [{"text": identity_prompt}]
    for msg in messages:
        parts.append({"text": msg.get("content", "")})

    payload = {"contents": [{"parts": parts}]}

    r = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)

    if r.status_code == 200:
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]

    return f"Error: {r.status_code}"
