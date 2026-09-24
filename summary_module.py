from gemini_client import generate_text
from utils import validate_text


def summarize_text(text: str) -> str:
    """
    Summarize educational text using Gemini.
    """

    text = validate_text(text)

    prompt = f"""
Summarize the following educational text.

Text:
{text}

Requirements:
- Be concise.
- Preserve the important information.
- Include the key points.
- Use simple language.
- Do not add information that is not present in the original text.
"""

    return generate_text(prompt)