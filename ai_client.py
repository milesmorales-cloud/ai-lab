import requests

from config import API_KEY, OPENROUTER_URL, MODEL


def send_message(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": messages,
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=data,
    )

    result = response.json()

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter error: {result}")

    return {
        "model": result["model"],
        "message": result["choices"][0]["message"]["content"],
    }