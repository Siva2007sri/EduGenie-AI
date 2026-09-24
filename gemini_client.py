from google import genai
from google.genai import types

from config import get_settings


def get_gemini_client():
    settings = get_settings()

    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Please add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_text(
    prompt: str,
    system_instruction: str | None = None,
    response_mime_type: str = "text/plain",
    temperature: float = 0.4,
) -> str:

    settings = get_settings()
    client = get_gemini_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        response_mime_type=response_mime_type,
    )

    if system_instruction:
        config.system_instruction = system_instruction

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=config,
    )

    if not response or not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text.strip()