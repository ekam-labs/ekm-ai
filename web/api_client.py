import requests


def fetch_ekm_data(BACKEND_URL, REQUEST_TIMEOUT, ekm_model, messages):

    try:
        payload = {
            "model": ekm_model,
            "messages": messages,
        }

        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 200:
            return response.json().get("res", "⚠️ Unexpected response format.")

        elif response.status_code == 429:
            return "⚠️ Too many requests — slow down. (429)"

        else:
            return f"❌ Error {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:
        return "❌ Request timed out. Try again later."

    except Exception as e:
        return f"❌ Failed to reach backend: {e}"