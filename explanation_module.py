from config import get_settings
from gemini_client import generate_text
from utils import validate_text


_local_pipeline = None


def explain_using_local_model(text: str) -> str:
    """
    Explain a concept using the local LaMini-Flan-T5 model.
    """

    global _local_pipeline

    if _local_pipeline is None:
        from transformers import pipeline

        _local_pipeline = pipeline(
            "text2text-generation",
            model=get_settings().LOCAL_EXPLANATION_MODEL,
        )

    prompt = f"""
Explain the following educational concept in simple language.

Concept:
{text}

Include:
1. Definition
2. Explanation
3. Example
4. One key point to remember
"""

    result = _local_pipeline(
        prompt,
        max_new_tokens=300,
        do_sample=False,
    )

    return result[0]["generated_text"]


def explain_concept(text: str) -> str:
    """
    Explain an educational concept.

    Gemini is used by default.
    If local mode is selected, the local model is attempted first.
    """

    text = validate_text(text)
    settings = get_settings()

    if settings.EXPLANATION_PROVIDER.lower() == "local":
        try:
            return explain_using_local_model(text)
        except Exception:
            # Fall back to Gemini if the local model cannot be loaded.
            pass

    prompt = f"""
You are an educational tutor.

Explain this concept clearly for a student:

{text}

Use this structure:

Definition:
...

Explanation:
...

Example:
...

Remember:
...

Requirements:
- Use simple language.
- Avoid unnecessary jargon.
- Make the explanation suitable for a student.
- Be accurate and clear.
"""

    return generate_text(prompt)