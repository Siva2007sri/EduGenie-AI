from gemini_client import generate_text
from utils import validate_text


def answer_question(text: str) -> str:
    """
    Answer the user's question using Gemini.
    """

    text = validate_text(text)

    prompt = f"""
You are EduGenie, an educational AI learning assistant.

Answer the user's question accurately and clearly.

User question:
{text}

Requirements:
- Give the direct answer first.
- Explain the answer briefly in simple language.
- Add an example when useful.
- Keep the response educational and easy to understand.
- Do not invent facts.
"""

    return generate_text(prompt)