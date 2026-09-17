import requests

from config import MODEL, OPENROUTER_API_KEY, OPENROUTER_URL


def send_message(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": messages,
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=data,
            timeout=30,
        )
    except requests.exceptions.RequestException as error:
        raise RuntimeError("Unable to connect to OpenRouter.") from error

    result = response.json()

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter error: {result}")

    return {
        "model": result["model"],
        "message": result["choices"][0]["message"]["content"],
    }


