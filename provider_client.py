from ai_client import send_message as send_openrouter_message
from gemini_client import send_with_fallback


def send_message(messages):
    try:
        return send_with_fallback(messages)
    except RuntimeError as gemini_error:
        try:
            return send_openrouter_message(messages)
        except RuntimeError as openrouter_error:
            raise RuntimeError(
                f"Gemini failed: {gemini_error}\n"
                f"OpenRouter failed: {openrouter_error}"
            ) from openrouter_error