import requests
from app.config import (GPT_MODEL, GROQ_API, LLAMA_SCOUT, MOONSHOT, QWEN,
                        REQUEST_TIMEOUT)


def call_groq(model_pick, messages, identity_prompt):

    url = "https://api.groq.com/openai/v1/chat/completions"

    if model_pick == "openai/gpt-oss-120b":
        selected_model = GPT_MODEL
    elif model_pick == "llama_scout":
        selected_model = LLAMA_SCOUT
    elif model_pick == "qwen":
        selected_model = QWEN
    else:
        return "Invalid Groq model"

    injected_messages = [{"role": "system", "content": identity_prompt}] + messages

    payload = {"model": selected_model, "messages": injected_messages}

    headers = {
        "Authorization": f"Bearer {GROQ_API}",
        "Content-Type": "application/json",
    }

    r = requests.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)

    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]

    return f"Error: {r.status_code}"
