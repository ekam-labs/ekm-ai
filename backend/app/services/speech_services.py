import requests
from app.config import GROQ_API


def transcribe_audio(audio_bytes):

    url = "https://api.groq.com/openai/v1/audio/transcriptions"

    headers = {
        "Authorization": f"Bearer {GROQ_API}"
    }

    files = {
        "file": ("audio.wav", audio_bytes)
    }

    data = {
        "model": "whisper-large-v3"
    }

    r = requests.post(url, headers=headers, files=files, data=data)

    if r.status_code == 200:
        return r.json()["text"]

    return f"Transcription failed: {r.status_code}"