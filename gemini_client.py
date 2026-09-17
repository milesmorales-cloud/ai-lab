import requests

from config import GEMINI_API_KEY

GEMINI_MODELS_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models"
)


def get_available_models():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    try:
        response = requests.get(
            GEMINI_MODELS_URL,
            params={"key": GEMINI_API_KEY},
            timeout=30,
        )
    except requests.exceptions.RequestException as error:
        raise RuntimeError("Unable to connect to Gemini.") from error

    result = response.json()

    if response.status_code != 200:
        raise RuntimeError(f"Gemini error: {result}")

    return result.get("models", [])

def get_text_models():
    models = get_available_models()

    models = [
        model
        for model in models
        if "generateContent" in model.get(
            "supportedGenerationMethods", []
        )
    ]

    preferred_model = "models/gemini-3.6-flash"

    return sorted(
        models,
        key=lambda model: model["name"] != preferred_model,
    ) 
   

def send_gemini_message(messages, model):
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    contents = []

    for message in messages:
        role = "model" if message["role"] == "assistant" else "user"

        contents.append({
            "role": role,
            "parts": [
                {
                    "text": message["content"]
                }
            ],
        })

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/{model}:generateContent"
    )

    data = {
        "contents": contents,
    }

    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            params={"key": GEMINI_API_KEY},
            json=data,
            timeout=30,
        )
    except requests.exceptions.RequestException as error:
        raise RuntimeError("Unable to connect to Gemini.") from error

    result = response.json()

    if response.status_code != 200:
        raise RuntimeError(f"Gemini error: {result}")

    return {
        "model": model,
        "message": result["candidates"][0]["content"]["parts"][0]["text"],
    }

 

def send_with_fallback(messages):
    candidates = get_text_models()

    last_error = None

    for model in candidates:
        try:
            return send_gemini_message(messages, model["name"])
        except RuntimeError as error:
            last_error = error

    raise RuntimeError(
        f"All Gemini models failed. Last error: {last_error}"
    )    