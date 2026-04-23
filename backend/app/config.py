import os

from dotenv import load_dotenv

load_dotenv()

REQUEST_TIMEOUT = 20

ALLOWED_MODELS = {
    "gemini-3-flash-preview",
    "gemini_2.5-flash",
    "gemma_v3",
    "openai/gpt-oss-120b",
    "llama_scout",
    "qwen",
}

GROQ_API = os.getenv("GROQ_API")
GPT_MODEL = os.getenv("GPT_MODEL")

GOOGLE_API = os.getenv("GOOGLE_API")
GEMINI3_FLASH = os.getenv("GEMINI3_FLASH")
GEMINI25_FLASH = os.getenv("GEMINI25_FLASH")
GEMMA3 = os.getenv("GEMMA3")

LLAMA_SCOUT = os.getenv("LLAMA_SCOUT")
QWEN = os.getenv("QWEN")
