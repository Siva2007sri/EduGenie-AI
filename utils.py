import json

from config import get_settings


def validate_text(text: str) -> str:
    """
    Validate and clean user input.
    """

    if not text or not text.strip():
        raise ValueError("Please enter some text.")

    cleaned_text = text.strip()

    settings = get_settings()

    if len(cleaned_text) > settings.MAX_INPUT_CHARS:
        raise ValueError(
            f"Input is too long. Maximum allowed length is "
            f"{settings.MAX_INPUT_CHARS} characters."
        )

    return cleaned_text


def clean_json_block(text: str) -> str:
    """
    Remove Markdown code fences and extract the JSON object/array.
    """

    cleaned = text.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    # Remove optional "json" prefix
    if cleaned.lower().startswith("json"):
        cleaned = cleaned[4:].strip()

    # Try to extract a JSON object
    object_start = cleaned.find("{")
    object_end = cleaned.rfind("}")

    if object_start != -1 and object_end != -1:
        return cleaned[object_start:object_end + 1]

    # Try to extract a JSON array
    array_start = cleaned.find("[")
    array_end = cleaned.rfind("]")

    if array_start != -1 and array_end != -1:
        return cleaned[array_start:array_end + 1]

    return cleaned


def parse_json_response(text: str):
    """
    Convert Gemini JSON text into a Python object.
    """

    cleaned = clean_json_block(text)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "The AI returned an invalid JSON response."
        ) from exc