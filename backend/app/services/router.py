from app.config import ALLOWED_MODELS
from app.prompts.identity import build_identity_prompt
from app.services.gemini_service import call_gemini
from app.services.groq_service import call_groq

def route_model(model_pick, messages):

    if model_pick not in ALLOWED_MODELS:
        return "Model not allowed."

    identity_prompt = build_identity_prompt(model_pick)

    if model_pick in ["gemini-3-flash-preview", "gemini_2.5-flash", "gemma_v3"]:
        return call_gemini(model_pick, messages, identity_prompt)

    if model_pick in ["openai/gpt-oss-120b", "moonshotai/kimi-k2-instruct-0905", "llama_scout", "qwen"]:
        return call_groq(model_pick, messages, identity_prompt)

    return "Invalid model"
